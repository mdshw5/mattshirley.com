# A Belated Introduction to pyfaidx
## Python module for efficient and convenient access to indexed FASTA files

When starting my current research project, I required random access to the human 
reference genome sequence, which is usually stored in a FASTA file. This is essentially 
a giant text file that is inconvenient to store in memory as a list of strings. My scripts 
were implemented in Python, and so the first solution to this problem was Brent Penderson's 
[pyfasta](https://github.com/brentp/pyfasta) module. pyfasta is a fine piece of software, 
but with a few limitations - primarily that the indexing scheme requires either creating a database 
or flattening (removing line breaks from) the FASTA file. Neither of these operations are ideal, 
considering the prefered indexing method for FASTA reference sequences was implemented in either 
[fastahack](https://github.com/ekg/fastahack) or [samtools](http://samtools.github.io) (I'm not sure which). 
Brent implemented a wrapper for fastahack called [python-fastahack](https://github.com/brentp/fastahack-python) 
and looking at the source for fastahack and samtools led me to believe that a pure Python 
fastahack implementation would be possible. 
The fastahack/samtools FASTA indexing scheme assumes that each entry in the file is line wrapped at a 
self-consistent (per entry) length. With this assumption met, an index can be created in the format:

```text
rname   rlen   offset   lenc   lenb
```

where for each entry (rname) in the FASTA file, the sequence length (rlen), byte offset in the file 
where that sequence starts (offset), line length in printable characters (lenc) and byte line 
length (lenb) are described. For example, hg19:

```text
chrMT   16569   7       70      71
chr1    249250621       16819   70      71
chr10   135534747       252828171       70      71
chr11   135006516       390299136       70      71
chr12   133851895       527234324       70      71
chr13   115169878       662998396       70      71
chr14   107349540       779813565       70      71
chr15   102531392       888696677       70      71
chr16   90354753        992692811       70      71
chr17   81195210        1084338354      70      71
chr18   78077248        1166693503      70      71
chr19   59128983        1245886148      70      71
chr2    243199373       1305859837      70      71
chr20   63025520        1552533494      70      71
chr21   48129895        1616459386      70      71
chr22   51304566        1665276858      70      71
chr3    198022430       1717314353      70      71
chr4    191154276       1918165681      70      71
chr5    180915260       2112050739      70      71
chr6    171115067       2295550509      70      71
chr7    159138663       2469110083      70      71
chr8    146364022       2630522162      70      71
chr9    141213431       2778977105      70      71
chrX    155270560       2922207877      70      71
chrY    59373566        3079696594      70      71
```

This file is stored alongside the FASTA file, traditionally with a `.fai` extension. With
the byte offset pointing to the start of each sequence, and the line byte length, we can calculate 
the number of bytes to read from any starting position which will return a subsequence from the file, 
including line breaks. These line breaks can be removed, and then we are left with the subsequence 
of interest. *None of this requires anything more than seek access to the file*.

I've implemented this indexing scheme in the [pyfaidx](https://github.com/mdshw5/pyfaidx) module, 
which is installable from PyPI. The name refers to the `samtools faidx` subcommand which implements 
similar functionality. The index files created by samtools, pyfaidx, and fastahack should all be compatible.
