import os
import streamlit as st
from streamlit.logger import get_logger
import google.generativeai as genai
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.agents import AgentExecutor, create_json_chat_agent

import pypdf

LOGGER = get_logger(__name__)
# Gemini APIキーの設定
genai.configure(api_key="AIzaSyBagYfwNZdCl-0yGMX1NvHuZelaC4SAZFg")

# Langsmith APIキーの設定
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__14d9d98ac88c42f69d2bc7a018792351"
os.environ["LANGCHAIN_PROJECT"] = "souzoku"

# Tavily  APIキーの設定
os.environ["TAVILY_API_KEY"] = "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"

# ツールの準備
tools = [TavilySearchResults(max_results=1)]
# プロンプトの準備
prompt = hub.pull("hwchase17/react-chat-json")
model = genai.GenerativeModel('gemini-pro')
# Construct the ReAct agent
agent = create_json_chat_agent(model, tools, prompt)

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Streamlit! 👋")

    st.sidebar.success("上のデモを選択してください。")

    st.markdown(
        """
         Streamlit は、以下のために特別に構築されたオープンソース アプリ フレームワークです。
        """
    )


    pdf_template = "法定相続情報一覧図の保管及び交付の申出書.pdf"
    pdf_output = "output.pdf" 

    pdf = pypdf.PdfReader(pdf_template)
#   pdfWriter = PyPDF2.PdfFileWriter()

    #st.write(pdf.get_fields())

    # フォームのフィールドに値を設定
    #pdfWriter.getFields()["name"] = "Taro Yamada"  
    #pdfWriter.getFields()["address"] = "Tokyo, Japan"  

    #pdfOutput = open(pdf_output, 'wb')
    #pdfWriter.write(pdfOutput)


    # Streamlitのインターフェース設定
    st.title('😱Generative AI with Google API')
    user_input = st.text_input("質問を入力してください:")

    if user_input:
        # モデルの設定

        # Create an agent executor by passing in the agent and tools
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        # ユーザーの入力をモデルに渡す

        result = agent_executor.invoke({"input": user_input})

        # 結果を表示
        st.write(result)



if __name__ == "__main__":
    run()
