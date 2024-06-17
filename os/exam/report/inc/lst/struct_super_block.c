struct super_block { // v 4.10
	struct list_head	s_list;		/* Keep this first */
	
	unsigned long		s_blocksize;
	loff_t			s_maxbytes;	/* Max file size */
	struct file_system_type	*s_type;
	const struct super_operations	*s_op;
	
	unsigned long		s_flags;
	
	unsigned long		s_magic;
	struct dentry		*s_root;
	struct rw_semaphore	s_umount;
	int			s_count;

	char s_id[32];				/* Informational name */
	
	const struct dentry_operations *s_d_op; /* default d_op for dentries */

	/*
	 * Keep the lru lists last in the structure so they always sit on their
	 * own individual cachelines.
	 */
	struct list_lru		s_dentry_lru ____cacheline_aligned_in_smp;
	struct list_lru		s_inode_lru ____cacheline_aligned_in_smp;
	
	struct list_head	s_inodes;	/* all inodes */

};