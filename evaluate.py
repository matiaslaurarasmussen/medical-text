__author__ = 'matias'

from search import StandardSolrEngine
from queryexpansion import AverageW2VExpansion
from evaluation.metrics import *
import logging


def evaluate(search_engine, k, verbose=False):
    with open('evaluation/data/findzebra.tsv','r') as infile:
        records = infile.read().split("\n")

        query_results = []

        for record in records:
            qid, query, answer, relevant, partly_relevant = record.split("\t")
            correct_answers = [ans for ans in relevant.split(",") + partly_relevant.split(",") if ans is not '']
            response = search_engine.query(query, top_n=k)
            returned_docids = [hit[u'id'] for hit in response.results]
            if verbose:
                print query
                print "P@%s" % (k,), precision(correct_answers,returned_docids)
                print "R@%s" % (k,), recall(correct_answers, returned_docids)
                print "F@%s" % (k,), f_measure(correct_answers, returned_docids)
            query_results.append((correct_answers, returned_docids))

        print str(search_engine)
        print "MAP", mean_average_precision(query_results)
        print "MRR", mean_reciprocal_rank(query_results)


if __name__ == "__main__":
    # setup logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # retrieval top k ranked
    k = 20
    search_engines = [
        StandardSolrEngine(),
        StandardSolrEngine(query_expansion=AverageW2VExpansion()),
        ]

    for engine in search_engines:
        evaluate(engine, k)