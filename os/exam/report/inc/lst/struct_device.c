struct device {
	struct device		*parent;
	struct kobject kobj;
	const char		*init_name; /* initial name of the device */
	const struct device_type *type;
	
	struct bus_type	*bus;		/* type of bus device is on */
	struct device_driver *driver;	/* which driver has allocated this
					   device */
					   
#ifdef CONFIG_NUMA
	int		numa_node;	/* NUMA node this device is close to */
#endif
	u64		*dma_mask;	/* dma mask (if dma'able device) */

	dev_t			devt;	/* dev_t, creates the sysfs "dev" */

};