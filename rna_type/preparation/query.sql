COPY(
	select
  xref.upi,
  dbid,
  xref.taxid as ac_taxid,
  ac.rna_type as ac_rna_type,
  layout.overlap_count,
  layout.sequence_coverage,
  models.taxid as model_taxid,
  models.so_term_id as r2dt_model_rna_type,
  rfam.so_rna_type as rfam_model_rna_type,
  pre.so_rna_type as rna_type,
  hits.sequence_stop,
  score
from xref
join rnc_accessions ac on xref.ac = ac.accession
join rnc_rna_precomputed pre on pre.upi = xref.upi and pre.taxid = xref.taxid
left join rnc_secondary_structure_layout layout on layout.urs = xref.upi
JOIN rnc_secondary_structure_layout_models models ON models.id = layout.model_id
LEFT JOIN rfam_model_hits hits on hits.upi = xref.upi
LEFT JOIN rfam_models rfam ON rfam.rfam_model_id = hits.rfam_model_id
where
  xref.deleted = 'N')
TO STDOUT with CSV DELIMITER ',' HEADER;
