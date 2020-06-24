echo "Taking accession numbers from $1"

# downloading gb files
python scripts/download_gb_files.py $1 gb

# extracting protein sequences
python scripts/gene_extraction gb fasta

# merging all fasta files into one file
cd fasta
touch all_seqs.fasta
for f in *.fa; do cat $f >> all_genes.fasta; done
cd ..

# creating the clustering folder
# making a database, clustering the data

mkdir clustering
cd clustering
mmseqs createdb ../fasta/all_genes.fasta DB
mmseqs cluster DB DB_clu tmp --threads $2 --min-seq-id 0.5 -c 0.8 --cov-mode 0
mmseqs createtsv DB DB DB_clu DB_clu.tsv
mmseqs createseqfiledb DB DB_clu DB_seqs_clustered
mmseqs result2flat DB DB DB_seqs_clustered ../fasta/clustered_seqs.fasta

cd ..
python scripts/extract_clusters.py clustering/DB_clu.tsv fasta/clustered_seqs.fasta fasta/clusters

# creating alignments

mkdir fasta/alignments
cd fasta/clusters
for f in *.fasta; do mafft --thread $2 --auto $f > ../alignments/$f; done

cd ../../
mkdir trees
cd trees
for f in ../fasta/alignments/*.fasta
do
    filename=$(basename -- "$f")
    filename="${filename%.*}"
    mkdir $filename
    cd $filename
    # replace raxmlHPC-PTHREADS-AVX with your version of raxml
    raxmlHPC-PTHREADS-AVX -s ../$f -T $2 -m PROTGAMMAAUTO -n $filename.out -N 100 -x $RANDOM -p $RANDOM
    cd ..
done

mkdir consensus

for f in cluster*
do
    cd $f
    # same thing here
    raxmlHPC-PTHREADS-AVX -J MR -z "RAxML_bootstrap.${f}.out" -T $2 -m PROTGAMMAAUTO -n $f
    cp RAxML_MajorityRuleConsensusTree.$f ../consensus
    cd ..
done

cd consensus
touch all_consensus_trees.txt
for f in RAxML_MajorityRuleConsensusTree.cluster*; do cat $f >> all_consensus_trees.txt; done
cd ..
python ../scripts/remove_annotations_on_trees.py consensus/all_consensus_trees.txt ../superdrzewa_soft/all_trees_for_fasturec.txt

cd ../superdrzewa_soft

./fasturec2 -Y -G all_trees_for_fasturec.txt -e a
mv fu.txt ../supertrees_list.txt
cd ..
python scripts/extract_tree.py supertrees_list.txt best_supertree.tre

echo "Resulting tree in best_supertree.tre file."



