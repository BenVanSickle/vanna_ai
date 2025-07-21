# requires python 3.11

from vanna.ollama import Ollama
from vanna.chromadb import ChromaDB_VectorStore
import os
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y%m%d %H%M%S')

train_model = os.environ.get('TRAIN_MODEL', 'false')
retrain_model = os.environ.get('RETRAIN_MODEL', 'false')

if retrain_model == 'true':
    train_model = 'true'
    os.system('rm chroma.sqlite3')

# The Ollama class already knows how to connect to a local ollama service
# The ChromaDB_VectorStore will store data. It will only need to be populated once and persists it.
class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        Ollama.__init__(self, config=config)
        vs = ChromaDB_VectorStore.__init__(self, config=config)


vn = MyVanna(config={'model': 'llama3'})

vn.connect_to_postgres(
    host='localhost',
    dbname='acquisition_development',
    user='acquisition__app',
    password='p@ssw0rd',
    port='5432'
)

if train_model == 'true':
    df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

    # This will break up the information schema into bite-sized chunks that can be referenced by the LLM
    plan = vn.get_training_plan_generic(df_information_schema)

    logging.info('Training...')
    vn.train(plan=plan)

    # This doesn't have to be Ruby ;-)
    os.system('ruby import_schema_list.rb')

    from schema_list import SCHEMA_LIST
    for table in SCHEMA_LIST:
        vn.train(ddl="""
            % s
        """ % table)

    logging.info('Training complete!')


if train_model != 'true':

    logging.info('running vannaFlaskApp')
    from vanna.flask import VannaFlaskApp

    app = VannaFlaskApp(vn, allow_llm_to_see_data = True)
    app.run()

os.system('TRAIN_MODEL=')
os.system('RETRAIN_MODEL=')