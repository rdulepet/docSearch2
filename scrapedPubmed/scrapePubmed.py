import pandas as pd
import numpy as np
import re
import time
from os.path import exists
import pickle
from requests.exceptions import ConnectionError
import logging

# Import libraries
import requests
from bs4 import BeautifulSoup

PUBMED_RESULTS_DIR = '../data/pubmed_results'
DATA_DIR = '../data'

logging.basicConfig(filename='process.log', encoding='utf-8', level=logging.DEBUG)

def fetch_num_citations(url):
    time.sleep(1)
    page = requests.get(url)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')
    
    relevant_cited_by_div = soup.find(class_='citedby-articles')
    
    if not relevant_cited_by_div:
        # done with page
        return 0
    
    relevant_amount_html = relevant_cited_by_div.find(class_='amount')
    for amount in relevant_amount_html:
        break

    return int(amount.replace(',', '').replace(' ', ''))

def scrape_pubmed_results(query):
    pubmed_articles = []
    pageno = 0
    ranking = 0
    
    SLEEP_TIME = 1

    while(True):
        pageno += 1
        url = f'https://pubmed.ncbi.nlm.nih.gov/?term={query}&filter=pubt.clinicalconference&filter=pubt.clinicalstudy&filter=pubt.clinicaltrial&filter=pubt.clinicaltrialprotocol&filter=pubt.clinicaltrialphasei&filter=pubt.clinicaltrialphaseii&filter=pubt.clinicaltrialphaseiii&filter=pubt.clinicaltrialphaseiv&filter=pubt.comparativestudy&filter=pubt.controlledclinicaltrial&filter=pubt.editorial&filter=pubt.meta-analysis&filter=pubt.observationalstudy&filter=pubt.practiceguideline&filter=pubt.pragmaticclinicaltrial&filter=pubt.randomizedcontrolledtrial&filter=pubt.researchsupportamericanrecoveryandreinvestmentact&filter=pubt.researchsupportnihextramural&filter=pubt.researchsupportnihintramural&filter=pubt.researchsupportnonusgovt&filter=pubt.researchsupportusgovtnonphs&filter=pubt.researchsupportusgovtphs&filter=pubt.researchsupportusgovernment&filter=pubt.validationstudy&show_snippets=off&size=200&page={pageno}&format=pubmed'
        #logging.info(f'\npage={pageno},url={url}')
        #logging.info(f'page={pageno}')
        NUM_TRIES = 3
        while NUM_TRIES > 0:
            try:
                time.sleep(SLEEP_TIME)
                page = requests.get(url)
                break
            except ConnectionError as e:    # This is the correct syntax
                logging.warning('RETRY AGAIN WITH HIGHER SLEEP, FAILED QUERY=%s, PAGE=%d', query, pageno)
                SLEEP_TIME += 5
                NUM_TRIES -= 1

        if NUM_TRIES == 0:
            # time to move on
            logging.error('DONE WITH RETRIES, FAILED QUERY=%s, PAGE=%d', query, pageno)
            break
            

        # Create a BeautifulSoup object
        soup = BeautifulSoup(page.text, 'html.parser')

        # Pull all text from the BodyText div
        relevant_pubmed_html = soup.find(class_='search-results-chunk')

        if not relevant_pubmed_html:
            # done with all pages
            break
        for pubmed_results in relevant_pubmed_html:
            break
        lines = pubmed_results.split('\r\n')
        #logging.info(f'lines_length={len(lines)}')

        article = None
        current_tag = ''

        try:
            for line in lines:
                line = line.strip()

                if line == '':
                    if article:
                        if len(article['authors']) > 1:
                            if article['authors'][-1]['affiliations'] == '':
                                article['authors'][-1]['affiliations'] = article['authors'][-2]['affiliations']

                        for idx, author in enumerate(article['authors']):
                            article['authors'][idx]['affiliations'] = article['authors'][idx]['affiliations'].split(';')
                            article['authors'][idx]['affiliations'] = [aff.strip() for aff in article['authors'][idx]['affiliations'] if aff != '']
                        article['citations'] = 0#fetch_num_citations(article['url'])
                        pubmed_articles.append(article)
                        article = None
                    current_tag = 'new'
                elif re.search(r'^PMID', line):
                    ranking += 1
                    article = {
                        'pmid':'', 
                        'pmc':'', 
                        'url':'', 
                        'title':'', 
                        'published_date':'', 
                        'abstract':'', 
                        'reference':'', 
                        'article_type':[], 
                        'authors':[], 
                        'journal':'', 
                        'mesh_terms':[], 
                        'citations': 0, 
                        'rank': ranking
                    }
                    article['pmid'] = re.sub(r'^PMID\s*\-\s+', '', line).strip()
                    article['url'] = f'https://pubmed.ncbi.nlm.nih.gov/{article["pmid"]}/'
                    current_tag = 'pmid'
                elif re.search(r'^PMC\s+\-\s+', line):
                    article['pmc'] = re.sub(r'^PMC\s+\-\s+', '', line).strip()
                    current_tag = 'pmc'
                elif re.search(r'^TI\s+\-\s+', line):
                    article['title'] = re.sub(r'^TI\s+\-\s+', '', line).strip()
                    current_tag = 'title'
                elif re.search(r'^DP\s+\-\s+', line):
                    article['published_date'] = re.sub(r'^DP\s+\-\s+', '', line).strip()
                    current_tag = 'published_date'
                elif re.search(r'^SO\s+\-\s+', line):
                    article['reference'] = re.sub(r'^SO\s+\-\s+', '', line).strip()
                    current_tag = 'reference'
                elif re.search(r'^AB\s+\-\s+', line):
                    article['abstract'] = re.sub(r'^AB\s+\-\s+', '', line).strip()
                    current_tag = 'abstract'
                elif re.search(r'^MHDA\s*\-\s*', line):
                    # ignore and skip it
                    current_tag = ''
                    continue
                elif re.search(r'^MH\s+\-\s+', line):
                    mesh_term = re.sub(r'^MH\s+\-\s+', '', line).strip()
                    mesh_term = re.sub(r'\*', '', mesh_term).strip()
                    article['mesh_terms'].append(mesh_term)
                    current_tag = 'mesh_terms'
                elif re.search(r'^PT\s+\-\s+', line):
                    article['article_type'].append(re.sub(r'^PT\s+\-\s+', '', line).strip())
                    current_tag = 'article_type'
                elif re.search(r'^JT\s+\-\s+', line):
                    article['journal'] = re.sub(r'^JT\s+\-\s+', '', line).strip()
                    current_tag = 'journal'
                elif re.search(r'^FAU\s+\-\s+', line):
                    if len(article['authors']) > 1:
                        if article['authors'][-1]['affiliations'] == '':
                            article['authors'][-1]['affiliations'] = article['authors'][-2]['affiliations']
                    article['authors'].append({
                        'full_name':re.sub(r'^FAU\s+\-\s+', '', line).strip(), 
                        'initial_name':'', 
                        'affiliations':''
                    })
                    current_tag = 'full_name'
                elif re.search(r'^AU\s+\-\s+', line):
                    article['authors'][-1]['initial_name'] = re.sub(r'^AU\s+\-\s+', '', line).strip()
                    current_tag = 'initial_name'
                elif re.search(r'^AD\s+\-\s+', line):
                    if current_tag == 'affiliations':
                        article['authors'][-1]['affiliations'] += ';'
                        article['authors'][-1]['affiliations'] += re.sub(r'^AD\s+\-\s+', '', line).strip()
                    else:
                        if len(article['authors']) == 0:
                            # seems like we arrived at AD without FAU, so assume no author but no name
                            article['authors'].append({
                                'full_name':'', 
                                'initial_name':'', 
                                'affiliations':''
                            })
                        #logging.info('1\t', article['authors'][-1]['affiliations'])
                        article['authors'][-1]['affiliations'] = re.sub(r'^AD\s*\-\s*', '', line).strip()
                        #logging.info('2\t', article['authors'][-1]['affiliations'])
                        current_tag = 'affiliations'
                elif re.search(r'^[A-Z]+\s*\-\s+', line):
                    # some tag that we don't care about so ignore,  and move on
                    current_tag = ''
                    continue
                elif current_tag == 'title':
                    article['title'] += ' '
                    article['title'] += re.sub(r'^TI\s+\-\s+', '', line).strip()
                elif current_tag == 'abstract':
                    article['abstract'] += ' '
                    article['abstract'] += re.sub(r'^AB\s+\-\s+', '', line).strip()
                    #article['abstract'] = re.sub(r'^BACKGROUND:\s*', '', article['abstract']).strip()
                elif current_tag == 'key_phrases':
                    key_phrase = re.sub(r'^MH\s+\-\s+', '', line).strip()
                    key_phrase = re.sub(r'\*', '', key_phrase).strip()
                    article['key_phrases'].append(key_phrase)
                elif current_tag == 'article_type':
                    article['article_type'].append(re.sub(r'^PT\s+\-\s+', '', line).strip())
                elif current_tag == 'affiliations':
                    article['authors'][-1]['affiliations'] += ' '
                    article['authors'][-1]['affiliations'] += re.sub(r'^AD\s+\-\s+', '', line).strip()
        except Exception as inst:
            logging.error('EXCEPTION: %s', line)
            logging.error(inst)
            logging.error(type(inst))    # the exception instance
            logging.error(inst.args)     # arguments stored in .args
            #raise inst
            pass
    
    df_pubmed_articles = pd.DataFrame(pubmed_articles)
    df_pubmed_articles.to_csv(f'{PUBMED_RESULTS_DIR}/{query}.csv', index=False)
    

def get_search_term_mapping():
    with open(f'{DATA_DIR}/who_search_terms_mapping.pkl', 'rb') as handle:
        out_search_space = pickle.load(handle)
        return out_search_space


search_space = get_search_term_mapping()
for key in search_space:
    vals = search_space[key]
    vals = [re.sub(r'\s*,\s*|\s*&\s*', ' ', val) for val in vals]
    vals = [re.sub(r'\s+', '+', val) for val in vals]
    key = re.sub(r'\s*,\s*|\s*&\s*', ' ', key)
    key = re.sub(r'\s+', '+', key)
    key = re.sub(r'\/|\\', '+', key)
    #logging.info(key, '--->', vals)
    
    if not exists(f'{PUBMED_RESULTS_DIR}/{key}.csv'):
        logging.info('scrape=%s', key)
        #scrape_pubmed_results(key)
    for val in vals:
        if not exists(f'{PUBMED_RESULTS_DIR}/{val}.csv'):
            logging.info('scrape=%s', val)
            #scrape_pubmed_results(val)
        

    
