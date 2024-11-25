#使用智谱嵌入方法实现数据向量化，数据存储位置为./data_base/knowledge_db
#并存储到Chroma向量库，存储路径为./data_base/vector_db/chroma

import os
from dotenv import load_dotenv, find_dotenv
from langchain.document_loaders.pdf import PyMuPDFLoader
from langchain.document_loaders.markdown import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from zhipuai_embedding import ZhipuAIEmbeddings
from langchain.vectorstores.chroma import Chroma

# 读取本地/项目的环境变量。
# find_dotenv()寻找并定位.env文件的路径
# load_dotenv()读取该.env文件，并将其中的环境变量加载到当前的运行环境中  
# 如果你设置的是全局的环境变量，这行代码则没有任何作用。
_ = load_dotenv(find_dotenv())



# 获取folder_path下所有文件路径，储存在file_paths里
file_paths = []
folder_path = './data_base/knowledge_db'
for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        file_paths.append(file_path)
print(file_paths[:3])




# 遍历文件路径并把实例化的loader存放在loaders里
loaders = []

for file_path in file_paths:

    file_type = file_path.split('.')[-1]
    if file_type == 'pdf':
        loaders.append(PyMuPDFLoader(file_path))
    elif file_type == 'md':
        loaders.append(UnstructuredMarkdownLoader(file_path))

# 下载文件并存储到text
texts = []
for loader in loaders: texts.extend(loader.load())

# 切分文档
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=50)

split_docs = text_splitter.split_documents(texts)

#构建Chroma向量库

# 定义 Embeddings
embedding = ZhipuAIEmbeddings()
# 定义持久化路径
persist_directory = './data_base/vector_db/chroma'

vectordb = Chroma.from_documents(
    documents=split_docs,
    embedding=embedding,
    persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
)
#保存数据库
vectordb.persist()