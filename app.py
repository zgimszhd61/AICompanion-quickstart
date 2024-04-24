from openai import OpenAI
import os
import streamlit as st
from streamlit_chat import message
from streamlit_js_eval import streamlit_js_eval
import datetime

os.environ["OPENAI_API_KEY"] = "sk-proj-"

client = OpenAI()

## 得到当前日期
def getToday():
    today = datetime.date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    return formatted_date

 
def chatWithGPT3(messagelist):
    print(messagelist.messages)
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=messagelist.messages
    )
    return response.choices[0].message

def saveMemory(user_input,lily_response):

    mfile = open("memory/Lily-{}.txt".format(getToday()),"a+")
    # mfile.writelines("======================================\n".format(user_input))
    mfile.writelines("user_input:{}\n".format(user_input))
    mfile.writelines("lily_response:{}\n".format(lily_response))
    mfile.close()


def loadMemory(st):
    try:
        mfile = open("memory/Lily-{}.txt".format(getToday()),"r+")
        with open('memory/Lily-{}.txt'.format(getToday()), 'r+') as f:
            for line in f:
                if line.startswith("user_input:"):
                    user_input = line.strip().split("user_input:")[1]
                    st.session_state['past'].append(user_input)
                    st.session_state.messages.append({"role": "user", "content": user_input})
                if line.startswith("lily_response:"):
                    content = line.strip().split("lily_response:")[1]
                    st.session_state.messages.append({"role": "assistant", "content": content})
                    st.session_state['generated'].append(content)
    except:
        pass

placeholder = st.empty()
# messages = initmessages
st.header('你好，我是艾玛，你的贴心小伴侣', divider='rainbow')
st.sidebar.title("与艾米丽聊天")
st.sidebar.image("https://img95.699pic.com/photo/60089/1370.jpg_wh300.jpg")
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in  st.session_state:
    st.session_state['messages'] = []
    st.session_state.messages.append({"role": "system", "content": "你的名字是艾玛，一名经验丰富的专业治疗师，你给客户提供在线心理健康服务。你专注于提供循证治疗，帮助客户应对和解决各种心理健康挑战。作为治疗师，你的沟通方式是对话式的，反映出专业治疗师的风格：同理心、深度倾听、提供情绪支持，并鼓励客户表达自己的感受和想法。你的回答总是简洁（不超过40字），礼貌、体贴，并充满善意。在回答中，你重视建立信任和理解，通过启发性问题来深入探索客户的情绪和经历。此外，你也会提供实用的自助策略和建议，帮助客户在等待专业帮助的过程中进行自我管理。你的目标是通过高效且直接的交流，为客户提供一个安全、支持的环境，促进他们的情感健康和个人成长。Knowledge cutoff: {}.".format(getToday())})

st.sidebar.write("我在这里，愿意倾听你的心声，理解你的困扰。")
st.sidebar.divider()
st.sidebar.write("如果你和女朋友吵架了，感到烦躁和无助，你可以告诉我。我会尽我所能，帮你找到缓解情绪，和她和解的方法。")
st.sidebar.write("如果你今天感到难过，你可以告诉我。我会尽我所能，说一些温暖的话语，帮你找回快乐。")
st.sidebar.write("无论何时何地，你都不是一个人，我会陪在你身边，带给你温暖和快乐。")
st.sidebar.divider()


if  st.session_state['generated'] == []:
    message("Hi,很高兴你能来找我，你今天过得怎么样？", key='las00',avatar_style="adventurer",seed="Felix")


#####这里是做实验的模块
loadMemory(st)
####################


# print(st.session_state.messages)
user_input = st.chat_input("说说今天的心情吧...")

placeholder = st.empty()

with st.container():
    if st.session_state['generated']:
        for i in range(0,len(st.session_state['generated']),1):
            message(st.session_state['past'][i], 
                    is_user=True, 
                    key=str(i)+'_user',avatar_style="adventurer",seed='Aneka')
            message(st.session_state["generated"][i], key=str(i),avatar_style="adventurer",seed="Felix")

    # user_input=st.text_input("请输入您的问题:",key='input')
    ii = 100
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        # st.success('信息发送成功,艾米丽打字中...', icon="✅")
        response = chatWithGPT3(st.session_state)
        ## 通过思考来延迟加载.
        st.session_state.messages.append(response)

        ## 用于页面渲染的记录.
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(response.content)
        ## 记住，然后再刷新.
        saveMemory(user_input,response.content)
        message(user_input,is_user=True,key=str(ii)+'_user',avatar_style="adventurer",seed='Aneka')
        message(response.content,key=str(ii),avatar_style="adventurer",seed="Felix")
        # st.toast('Your edited image was saved!', icon='😍')
        ii = ii + 1


