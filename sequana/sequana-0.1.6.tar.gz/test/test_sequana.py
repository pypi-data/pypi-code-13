from sequana import sequana_data


def test_sequana_data():

    try:
        sequana_data()
        assert False
    except ValueError:
        assert True
    except:
        assert False 

    sequana_data("Hm2_GTGAAA_L005_R1_001.fastq.gz", "data")
