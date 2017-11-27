import urllib.request
from xml.etree import ElementTree


class GEODataSet:

    def __init__(self,accession):
        self.accession = accession
        self.title = "No title"
        self.summary = "No summary"
        self.type = "No type"
        self.species = "No species"

        # Samples will be a dictionary indexed by accession
        self.samples = {}


        # Try to do a fetch for eutils ids for this accession

        # We'll collect the eutils UIDs we find so that we can construct the
        # details query later on.
        eutilAccessions = []

        with urllib.request.urlopen('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term={}&field=GEO%20Accession'.format(accession)) as response:
            gdsXML = ElementTree.fromstring(response.read())
            for child in gdsXML:
                if child.tag == 'IdList':
                    for geoid in child:
                        eutilAccessions.append(int(geoid.text))



        if len(eutilAccessions) == 0:
            raise FileNotFoundError('No samples found for {}'.format(accession))


        # We can now do the second query against esummary
        with urllib.request.urlopen('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&id={}'.format(','.join(str(uid) for uid in eutilAccessions))) as response:
            uidXML = ElementTree.fromstring(response.read())

        for document in uidXML:
            # We don't want the platform entries
            if document[1].text[0:3] == 'GPL':
                #print("Skipping platform")
                continue

            elif document[1].text[0:3] == 'GSE':
                # We can parse information about the series
                for item in document:
                    if item.tag != 'Item':
                        continue

                    if item.attrib['Name'] == 'title':
                        self.title = item.text

                    elif item.attrib['Name'] == 'summary':
                        self.summary = item.text

                    elif item.attrib['Name'] == 'gdsType':
                        self.type = item.text

                    elif item.attrib['Name'] == 'taxon':
                        self.species = item.text


                    elif item.attrib['Name'] == 'Samples':
                        for sample in item:
                            gs = self.getSampleByAccession(sample[0].text)
                            gs.name = sample[1].text



            elif document[1].text[0:3] == 'GSM':
                # We need to get the sample object first
                sample = self.getSampleByAccession(document[1].text)

                for item in document:
                    if item.tag != 'Item':
                        continue

                    if item.attrib['Name'] == 'title':
                        sample.name = item.text

                    elif item.attrib['Name'] == 'summary':
                        sample.summary = item.text

                    elif item.attrib['Name'] == 'taxon':
                        sample.species = item.text

                    elif item.attrib['Name'] == 'ExtRelations':
                        for external in item[0]:
                            if external.attrib['Name'] == 'TargetObject':
                                sample.sra_accession = external.text


    def getSampleByAccession(self,accession):
        if not accession in self.samples:
            self.samples[accession] = GEOSample(accession)

        return self.samples[accession]



    def all_samples (self):
        for value in self.samples.values():
            yield value

class GEOSample:
    def __init__(self,accession):
        self.accession = accession
        self.name = "No name"
        self.species = "No species"
        self.summary = "No summary"
        self.sra_accession = "No SRA accession"
