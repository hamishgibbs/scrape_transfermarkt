if [ $# -eq 0 ]; then
  echo "Specify the number of cores --cores {}."
  exit 1
fi

snakemake --cores $1 concat_teams --rerun-incomplete
snakemake --cores $1 concat_games --rerun-incomplete
snakemake --cores $1 concat_match_sheets --rerun-incomplete
snakemake --cores $1 concat_stadiums --rerun-incomplete
snakemake --cores $1 --rerun-incomplete