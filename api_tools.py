import requests
import json

def search_pubmed(query, num_results=5):
    """Search PubMed for articles and return summaries with calculated relevance (keyword count)."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pubmed',
        'term': query,
        'retmax': num_results,
        'retmode': 'json'
    }
    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        ids = data['esearchresult']['idlist']
        summaries = []
        for id in ids:
            summary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={id}&retmode=json"
            summary_response = requests.get(summary_url, timeout=5)
            if summary_response.status_code == 200:
                summary_data = summary_response.json()
                title = summary_data['result'][id].get('title', 'No title')
                relevance = title.lower().count(query.lower())
                summaries.append({'id': id, 'title': title, 'relevance': relevance})
        return {'results': summaries}
    except Exception as e:
        return {'error': f'PubMed search failed: {str(e)}'}

def search_rxnorm(drug_name):
    """Map drug to RxNorm codes and compute therapeutic classes."""
    base_url = "https://rxnav.nlm.nih.gov/REST/rxcui.json"
    params = {'name': drug_name}
    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        rxcui = data.get('idGroup', {}).get('rxnormId', [None])[0]
        if rxcui:
            info_url = f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/properties.json"
            info_response = requests.get(info_url, timeout=5)
            if info_response.status_code == 200:
                info_data = info_response.json()
                properties = info_data.get('properties', {})
                classes = properties.get('therapeuticClasses', []) or ['Unknown']
                return {'rxcui': rxcui, 'properties': properties, 'therapeutic_classes_count': len(classes)}
        return {'error': 'No RxCUI found'}
    except Exception as e:
        return {'error': f'RxNorm search failed: {str(e)}'}

def search_mesh(term):
    """Link term to MeSH headings and calculate match count."""
    base_url = "https://id.nlm.nih.gov/mesh/sparql"
    query = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?mesh ?label
    WHERE {{
        ?mesh rdfs:label ?label .
        FILTER (regex(?label, "{term}", "i"))
    }}
    LIMIT 5
    """
    params = {'query': query, 'format': 'json'}
    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        terms = [{'uri': item['mesh']['value'], 'label': item['label']['value']} for item in data['results']['bindings']]
        return {'terms': terms, 'match_count': len(terms)}
    except Exception as e:
        return {'error': f'MeSH search failed: {str(e)}'}

def search_openfda(drug_name, limit=5):
    """Fetch OpenFDA adverse events and calculate frequency stats."""
    base_url = "https://api.fda.gov/drug/event.json"
    params = {'search': f'patient.drug.openfda.brand_name:"{drug_name}"', 'limit': limit}
    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data['meta']['results']['total'] > 0:
            events = data['results']
            reactions = [reaction for event in events for reaction in event.get('patient', {}).get('reaction', [])]
            unique_reactions = set(reaction['reactionmeddrapt'] for reaction in reactions if 'reactionmeddrapt' in reaction)
            return {'events': events, 'unique_reactions_count': len(unique_reactions)}
        return {'error': 'No OpenFDA data found'}
    except Exception as e:
        return {'error': f'OpenFDA search failed: {str(e)}'}