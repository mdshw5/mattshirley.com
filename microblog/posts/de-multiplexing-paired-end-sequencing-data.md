title: De-multiplexing paired-end sequencing data
link: /de-multiplexing-paired-end-sequencing-data/
creator: matt
description: 
post_id: 257
post_date: 2012-09-04 13:32:05
post_date_gmt: 2012-09-04 17:32:05
comment_status: open
post_name: de-multiplexing-paired-end-sequencing-data
status: publish
post_type: post

# De-multiplexing paired-end sequencing data

After surveying the existing tools for de-multiplexing barcoded paired-end sequencing reads, I grew frustrated and rolled my own solution. The issue with most of the tools for de-multiplexing reads from massively parallel sequencing is that they operate on fastq files. Since paired-end sequencing typically generates two fastq files (one for forward reads and one for reverse reads), it becomes more difficult to apply [existing](http://hannonlab.cshl.edu/fastx_toolkit/commandline.html#fastx_barcode_splitter_usage) single-end read tools without doing some extra matching and filtering. Most people seem to either:

  1. Merge the forward and reverse reads into one "megaread", demultiplex these based on barcode sequence, and then split the resulting reads back into forward and reverse before mapping.
  2. Filter the forward reads based on barcodes, and take advantage of same sorting order of forward and reverse reads to match pairs from the reverse reads.

Both of these routes involve creating many individual fastq files that will be individually mapped. Depending on the aligner and amount of sequence, mapping something like 75 de-multiplexed sets of reads could be inefficient since you would be initializing the aligner and indexed reference genome 75 times. This does not seem like an optimal solution.

Since my immediate purpose is amplicon resequencing on a [MiSeq](http://www.illumina.com/systems/miseq.ilmn), the number of reads I will be dealing with is fairly low, so I think I can design a more logical workflow. Ideally, I would like to map all the reads at once, moving the barcode from each read into the SAM [BC](http://samtools.sourceforge.net/SAM1.pdf) tag. Then I can split the resulting mapped SAM file into de-multiplexed files for analysis.

First off, mapping my reads with BWA. I'm using [Bpipe](http://code.google.com/p/bpipe/) for pipeline management.
    
    @Transform("sam")
    bwa_aln_bc = {
        exec "bwa aln -t $threads -B $length $bwa_reference $input1 > ${input1}.sai"
        exec "bwa aln -t $threads  $bwa_reference $input2 > ${input2}.sai"
        exec "bwa sampe $bwa_reference ${input1}.sai ${input2}.sai $input1 $input2 > $output"
    }

 The above function truncates $length number of bases from each forward read, and assigns that as a BC tag in the resulting SAM alignment e.g.: "BC:Z:TTAATGC".

Next, we will split the barcoded SAM file into multiple files, based on the barcodes, while preserving the SAM header. All reads that do not match a barcode in the supplied table will be written to a separate file.
    
    #!/bin/sh
    if [ $# -eq 0 ] ; then
        echo 'Usage: splitSam.sh input.sam barcodes.txt'
        echo ''
        echo 'barcodes.txt must be two columns with tab delimeter'
        echo 'column1 = barcode name, column2 = barcode sequence'
    fi
    SAM=$1
    BC_FILE=$2
    
    #Capture the SAM header
    SAM_H=`samtools view -SH $SAM`
    
    #Read barcode table into array line by line
    #then grep barcoded SAM reads to file
    while IFS=$'\t' read -r -a array
    do
        sampleName=${array[0]} #barcode name
        BC=${array[1]} #barcode sequence
        BC=${BC%"${BC##*[![:space:]]}"} #remove trailing whitespace
        if grep -q -m 1 -e "BC:Z:$BC" $SAM; then
            printf "$SAM_H\n" > ${sampleName}.sam #write SAM header to file
            grep -e "BC:Z:$BC" $SAM >> ${sampleName}.sam #write barcoded reads
        fi
        printf "BC:Z:$BC\n" >> /tmp/bc #patterns for unmatched reads
    done < $BC_FILE
    
    #Write unmatched reads to file
    grep -v -f /tmp/bc $SAM > unmatched.sam #write unmatched reads
    rm /tmp/bc

This approach, while efficient for a small number of reads, may be inappropriate for larger projects.