# Masking low-complexity regions using pyfaidx MutableFastaRecord
Masking a sequence is simply the process of changing some letters of the sequence to another character, or capitalization. 
All FASTA masking tools that I can find (such as bedtools [maskfasta](http://bedtools.readthedocs.org/en/latest/content/tools/maskfasta.html) seem to read
an entire file, or entire records in a file, and the perform character replacement in order from start to end of the file. 
This strategy requires that the list of regions (potentially specified in a BED file) are sorted in the same way 
as the FASTA file, or that the regions are all stored in memory. Also, the entire FASTA file must be read, and then 
subsequently modified and written back to disk. This round trip seems unnecessary if you can just modify the FASTA file 
in place. Therefore, I started thinking about the safest way to modify the sequence content of a FASTA file on-disk while 
maintaining the original line breaks and line wrapping length. The result is the [pyfaidx](https://github.com/mdshw5/pyfaidx) 
MutableFastaRecord. As an example of this in-place modification of a FASTA file I decided to mask low-complexity regions of the human genome. 

Heng Li's recent publication describing genomic regions with [high variant calling artifacts](http://arxiv.org/abs/1404.0929) 
provides a definition of low-complexity regions to filter for variant calling, along with a [BED file for download](http://arxiv.org/abs/1404.0929). Using this bed file, the [GRCv37](ftp://ftp.1000genomes.ebi.ac.uk//vol1/ftp/technical/reference/human_g1k_v37.fasta.gz) human reference genome,
and a [script] that will be included in the next version of pyfaidx, 
I benchmarked my in-place FASTA masking against bedtools maskfasta. Below is the main function of the script:

```python
def mask_sequence(args):
    assert len(args.default_seq) == 1
    fasta = Fasta(args.fasta, mutable=True) 
    for line in args.bed:
        rname, start, end = bed_split(line)
        # fasta[rname] will return a MutableFastaRecord object
        if args.action == 'replace':
            fasta[rname][start:end] = (end - start) * args.default_seq
        elif args.action == 'lowercase':
            fasta[rname][start:end] = fasta[rname][start:end].lowercase()
```

As you can see, `fasta[rname][start:end]` is a slice of a MutableFastaRecord object, which when called alone 
uses the `__getitem__` method and when assigned a value uses the `__setitem__` method. The `__getitem__` method 
fetches the sequence (without line breaks) from the FASTA file. The `__setitem__` method writes the sequence 
*including the line breaks in the file, as they appear on disk*. Timings for both methods:

### bedtools maskfasta
2 minutes, 7 seconds  
661 MB max memory usage  
98% CPU usage

### pyfaidx bedmask
1 minute 32 seconds  
121 MB max memory usage  
78% CPU usage

Two things to note:  

1. At such small runtimes this process does not *really* need optimization 
2. The in-place masking 
runtime should scale with the number and length of regions to mask. For a small number of regions the operation will 
be almost instantaneous. For extensive masking, covering most of the file, the overhead of seeking, reading and then writing 
to/from the file for each region will overcome the performance gain over the streaming method.
