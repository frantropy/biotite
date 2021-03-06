# This source code is part of the Biotite package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

import itertools
import numpy as np
from requests.exceptions import ConnectionError
import pytest
import biotite
import biotite.database.entrez as entrez
import biotite.sequence.io.fasta as fasta
from biotite.database import RequestError


@pytest.mark.xfail(raises=ConnectionError)
@pytest.mark.parametrize(
    "common_name, as_file_like",
    itertools.product([False, True], [False, True])
)
def test_fetch(common_name, as_file_like):
    path = None if as_file_like else biotite.temp_dir()
    db_name = "Protein" if common_name else "protein"
    file = entrez.fetch("1L2Y_A", path, "fa", db_name,
                        "fasta", overwrite=True)
    fasta_file = fasta.FastaFile()
    fasta_file.read(file)
    prot_seq = fasta.get_sequence(fasta_file)

@pytest.mark.xfail(raises=ConnectionError)
@pytest.mark.parametrize("as_file_like", [False, True])
def test_fetch_single_file(as_file_like):
    file_name = None if as_file_like else biotite.temp_file("fa")
    file = entrez.fetch_single_file(
        ["1L2Y_A", "3O5R_A"], file_name, "protein", "fasta"
    )
    fasta_file = fasta.FastaFile()
    fasta_file.read(file)
    prot_seqs = fasta.get_sequences(fasta_file)
    assert len(prot_seqs) == 2

@pytest.mark.xfail(raises=ConnectionError)
def test_fetch_invalid():
    with pytest.raises(RequestError):
        file = entrez.fetch("xxxx", biotite.temp_dir(), "fa", "protein",
                            "fasta", overwrite=True)