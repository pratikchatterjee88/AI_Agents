from openai import OpenAI
import streamlit as st
import ollama
from fpdf import FPDF
import base64

# First let's do an import
from dotenv import load_dotenv
load_dotenv(override=True)

openai = OpenAI()
ollama = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

st.set_page_config(page_title="Agentic AI Ideation Tool", layout="wide")

st.title("🤖 Agentic AI Business Opportunity Generator")
st.markdown("Turn industry pain points into AI-powered business ideas and solutions. 💡")

#Initialize session state variable . This will make sure that all outputs are stored in the session state and can be used in the next steps.

for key in ["business_idea", "pain_points", "final_AI_soln"]:
     if key not in st.session_state:
          st.session_state[key] = ""

#Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [ "Step 1: Business Opportunity", "Step 2: Pain Points", "Step 3: AI Solution"])


#Progress Indicator
st.sidebar.subheader("Progress")
st.sidebar.markdown(f"**Step 1:** {'✔️' if st.session_state.business_idea else '❌'}")
st.sidebar.markdown(f"**Step 2:** {'✔️' if st.session_state.pain_points else '❌'}")
st.sidebar.markdown(f"**Step 3:** {'✔️' if st.session_state.final_AI_soln else '❌'}")


#Reset Session
if st.sidebar.button("🔁 Start New Session"):
     for key in st.session_state.keys():
          del st.session_state[key]
     st.rerun()


#PDF Download Function
def generate_pdf(business, pain, solution):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, "Agentic AI Business Ideator Results\n", align="C")
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Step 1: Business Opportunity\n{business}", align="L")
    pdf.multi_cell(0, 10, f"Step 2: Pain Points\n{pain}\n\n")
    pdf.multi_cell(0, 10, f"Step 3: Agentic AI Solution\n{solution}\n\n")
    
    return pdf.output(dest="S").encode("latin1")

def download_button():
    if st.session_state.business_idea and st.session_state.pain_points and st.session_state.final_AI_soln:
        pdf_bytes = generate_pdf(
            st.session_state.business_idea,
            st.session_state.pain_points,
            st.session_state.final_AI_soln,
        )
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="agentic_ai_idea.pdf">📥 Download Report as PDF</a>'
        st.markdown(href, unsafe_allow_html=True)


#Step1: Business area Input
if page == "Step 1: Business Opportunity":
     st.header("step 1: Discover a Business Opportunity")
     industry  =st.text_input("Enter an industry or area you're curious about:", placeholder="e.g., Healthcare, Finance, Education, Retail Automation, Customer Journey")

     if st.button("Generate Business Idea"):
        with st.spinner("Thinking..."):
            question = (
                f"Help me with a compelling business area in {industry} where Agentic AI should excel and with easy workflows."
                "and automations can build a monetary value. I want to see areas of opportunity that are not obivious to the human eye."
            )
            message = [{"role": "user", "content": question}]
            response = ollama.chat.completions.create(model="llama3.2", messages=message)
            st.session_state.business_idea = response.choices[0].message.content
        
     if st.session_state.business_idea:
        st.subheader("💡 Business idea:")
        st.markdown(st.session_state.business_idea)


# Step 2: Pain point identification

elif page == "Step 2: Pain Points":
     st.header("step 2: Identify Pain Points")

     if not st.session_state.business_idea:
        st.warning("Please generate a business idea first.")
     else:
        with st.spinner("Analyzing pain points..."):
            pain_question = "What do you think cound be the pain points of the customers within the industry, where agentic solution can help?"
        
            message = [{"role": "user", "content": pain_question + "\n\n" + st.session_state["business_idea"]}]
            response = ollama.chat.completions.create(model="llama3.2", messages=message)
            
            st.session_state.pain_points = response.choices[0].message.content


     if st.session_state.pain_points:
        st.subheader("💡 Pain Points Identified:")
        st.markdown(st.session_state.pain_points)


# Step 3: AI-powered solution
elif page == "Step 3: AI Solution":
    st.header("Step 3: Propose an Agentic AI Solution")


    if not st.session_state.pain_points:
            st.warning("Please analyze pain points first.")
    else:
                if st.button("Generate AI- Powered Solution"):
                    with st.spinner("Designing Intelligent Agentic Solution..."):
                        solution_question = "Propose an Agentic AI solution for the pain points."
                        message = [{"role": "user", "content": solution_question + "\n\n" + st.session_state["pain_points"]}]
                        response = ollama.chat.completions.create(model="llama3.2", messages=message)
                        st.session_state.final_AI_soln = response.choices[0].message.content

                if st.session_state.final_AI_soln:
                    st.subheader("💡 Agentic AI Solution:")
                    st.markdown(st.session_state.final_AI_soln)

                
                download_button()
            
    
                




