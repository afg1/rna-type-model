"""
This file defines all the label functions I can think of that will give semi decent labelling of RNA type.
"""

from snorkel.labeling import labeling_function


from .labels import RNATypeCoarse
from rna_type.utils.ontology_tests import (
    is_child_of,
    same_domain,
    specificity,
    lowest_common_ancestor,
)
import numpy as np


@labeling_function()
def score_based(x):
    """
    Based on looking at the score distribution (without any knowledge of the model providing the score)
    this seems like a fairly good discriminator. x will be a dataframe row of lists, so need to use the any
    function in the ifs
    """

    try:
        score = [float(s) for s in x["score"]]
    except ValueError:
        print(x)
        raise ValueError
    if any([s > 500 for s in score]):
        return RNATypeCoarse.tRNA
    elif any([s < 500 for s in score]):
        return RNATypeCoarse.abstain
    else:
        return RNATypeCoarse.rRNA


@labeling_function()
def accession_based(x):
    """
    look at the accession rna types and see which it is a child of, then return that if the accession is trustworthy
    """
    trusted = [4, 8, 16, 18, 20, 24, 37]

    ## Count the number of trusted sources for this URS
    n_trusted = len(set(trusted).intersection(set(x["dbid"])))

    ## If no trusted sources, abstain
    if n_trusted == 0:
        return RNATypeCoarse.abstain
    ## If only one, use that
    elif n_trusted == 1:
        trusted_id = list(set(trusted).intersection(set(x["dbid"])))[0]
        rna_type = x["ac_rna_type"][np.where(x["dbid"] == trusted_id)][0]
        if is_child_of("SO:0000252", rna_type):  ## rRNA
            return RNATypeCoarse.rRNA
        elif is_child_of("SO:0000253", rna_type):  ## tRNA
            return RNATypeCoarse.tRNA
        else:
            return RNATypeCoarse.other
    ## If more than one, look at  whether they agree
    else:
        trusted_ids = list(set(trusted).intersection(set(x["dbid"])))
        rna_types = x["ac_rna_type"][
            np.where([db == tr for db, tr in zip(x["dbid"], trusted_ids)])
        ]

        rRNA_agreement = [is_child_of("SO:0000252", t) for t in rna_types]
        tRNA_agreement = [is_child_of("SO:0000253", t) for t in rna_types]

        other_aggreement = [
            not r and not t for r, t in zip(rRNA_agreement, tRNA_agreement)
        ]

        if all(rRNA_agreement):
            return RNATypeCoarse.rRNA
        elif all(tRNA_agreement):
            return RNATypeCoarse.tRNA
        elif all(other_aggreement):
            return RNATypeCoarse.other
        else:
            return RNATypeCoarse.abstain


@labeling_function()
def passthrough(x):
    """
    If a URS only has one accession, just pass through the type of it without anything fancy, else abstain

    Equivalent to the first test in the current type determination
    """
    if len(x["dbid"] == 1):
        rna_type = x["ac_rna_type"][0]
        if is_child_of("SO:0000252", rna_type):  ## rRNA
            return RNATypeCoarse.rRNA
        elif is_child_of("SO:0000253", rna_type):  ## tRNA
            return RNATypeCoarse.tRNA
        else:
            return RNATypeCoarse.other

    else:
        return RNATypeCoarse.abstain


@labeling_function()
def is_lncRNA(x):
    """
    Return other if we have an accession that says its a lncRNA and that accession comes from somewhere sensible

    Sensible = DBs that measure expression, DBs that deal only with lncRNA, DBs that link to literature
    (so Expression Atlas, PLncDB, GeneCards, MalaCards, IntAct, LncBook, maybe others?)
    """
    lnc_trusted = [51, 50, 33, 40, 41, 42]
    n_trusted = len(set(lnc_trusted).intersection(set(x["dbid"])))
    if n_trusted == 0:
        return RNATypeCoarse.abstain
    else:
        rna_types = x["ac_rna_type"][
            np.where([db == tr for db, tr in zip(x["dbid"], lnc_trusted)])
        ]
        if "SO:0001877" in rna_types:
            return RNATypeCoarse.other
        else:
            return RNATypeCoarse.abstain


@labeling_function()
def is_miRNA(x):
    """
    Return other if we have an accession that says its a miRNA and that accession comes from somewhere sensible

    Sensible = DBs that measure expression, DBs that deal only with lncRNA, DBs that link to literature
    (so Expression Atlas, miRbase, GeneCards, MalaCards, IntAct, LncBook, maybe others?)
    """
    mi_trusted = [51, 4, 33, 40, 41, 42]
    n_trusted = len(set(mi_trusted).intersection(set(x["dbid"])))
    if n_trusted == 0:
        return RNATypeCoarse.abstain
    else:
        rna_types = x["ac_rna_type"][
            np.where([db == tr for db, tr in zip(x["dbid"], mi_trusted)])
        ]
        if "SO:0000276" in rna_types:
            return RNATypeCoarse.other
        else:
            return RNATypeCoarse.abstain


@labeling_function()
def coverage_based(x):
    """
    Based on sequence coverage, which I think comes from the r2dt hits.
    From looking at histograms of the accessions, only rRNAs have coverage below 0.3
    """
    if all([cov <= 0.3 for cov in x["sequence_coverage"]]):
        return RNATypeCoarse.rRNA
    else:
        return RNATypeCoarse.abstain


@labeling_function()
def length_based(x):
    """
    From a quick look, I think most tRNAs are below 100 nt long

    This will for sure mislabel miRNAs and other short things, so we would need a counter example
    """
    if all([l < 100 for l in x["sequence_stop"]]) and all(
        [l > 35 for l in x["sequence_stop"]]
    ):
        return RNATypeCoarse.tRNA
    elif all([l <= 35 for l in x["sequence_stop"]]):
        return RNATypeCoarse.other
    else:
        return RNATypeCoarse.abstain


def pairing_based(x):
    """
    rRNAs have more loops, do they have a higher fraction of unpaired bases?
    """
    pass


@labeling_function()
def taxonomy_based_r2dt(x):
    """
    Look at the taxonomy of the hit and the accession. If it doesn't make 'sense' then don't yield the accession

    Sense is defined as:
    - Coming from the same superkingdom
    - bacterial hits in mitochondrial genomes
    - Other things yet to be decided...

    So e.g. a bacterial Rfam/r2dt hit in an accession from human only makes sense if the hit is in the mitochondria

    TODO: need some more data to be able to get the mt hits exclusion
    """

    ## look at hits - if all are within the same doimain, its probably legit, check type and return
    domain_similarity = [
        same_domain(acc_tax, mod_tax)
        for acc_tax, mod_tax in zip(x["ac_taxid"], x["model_taxid"])
    ]
    if any(domain_similarity):
        acc_type = x["r2dt_model_rna_type"][0]
        if is_child_of("SO:0000252", acc_type):  ## rRNA
            return RNATypeCoarse.rRNA
        elif is_child_of("SO:0000253", acc_type):  ## tRNA
            return RNATypeCoarse.tRNA
        else:
            return RNATypeCoarse.other
    else:
        ## At least one hit comes from a domain different to the organism.
        ## In this case, we should look at the source of the hit, i.e. is it mitochondrial
        ## This is actually a lot more complicated than I thought. chromosomes is probably the right place
        ## to look, but the naming is not how I thought - would need lookups to NCBI and stuff. Maybe a data enrichment
        ## project for after release, but right now, no thank you.

        return RNATypeCoarse.abstain


@labeling_function()
def taxonomy_based_rfam(x):
    """
    Look at the taxonomy of the hit and the accession. If it doesn't make 'sense' then don't yield the accession

    Sense is defined as:
    - Coming from the same superkingdom
    - bacterial hits in mitochondrial genomes
    - Other things yet to be decided...

    So e.g. a bacterial Rfam/r2dt hit in an accession from human only makes sense if the hit is in the mitochondria

    TODO: need some more data to be able to get the mt hits exclusion
    """

    ## look at hits - if all are within the same doimain, its probably legit, check type and return
    domain_similarity = [
        same_domain(acc_tax, mod_tax)
        for acc_tax, mod_tax in zip(x["ac_taxid"], x["model_taxid"])
    ]
    if any(domain_similarity):
        acc_type = x["rfam_model_rna_type"][0]
        if is_child_of("SO:0000252", acc_type):  ## rRNA
            return RNATypeCoarse.rRNA
        elif is_child_of("SO:0000253", acc_type):  ## tRNA
            return RNATypeCoarse.tRNA
        else:
            return RNATypeCoarse.other
    else:
        ## At least one hit comes from a domain different to the organism.
        ## In this case, we should look at the source of the hit, i.e. is it mitochondrial
        ## This is actually a lot more complicated than I thought. chromosomes is probably the right place
        ## to look, but the naming is not how I thought - would need lookups to NCBI and stuff. Maybe a data enrichment
        ## project for after release, but right now, no thank you.

        return RNATypeCoarse.abstain
