import pytest
import project1.main as project1
import argparse

def test_inputData():
    args = argparse.Namespace(input=['*.txt'])
    inputData = project1.inputFiles(args)
    assert len(inputData)>0