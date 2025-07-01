import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
import datetime
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.metric_cards import style_metric_cards

# Custom CSS for ultra-modern styling
def local_css():
    st.markdown("""
    <style>
    /* Main styles */
    :root {
        --primary: #6e8efb;
        --secondary: #a777e3;
        --dark: #2d3748;
        --light: #f7fafc;
        --success: #48bb78;
        --warning: #ed8936;
        --danger: #f56565;
        --info: #4299e1;
    }
    
    /* General styling */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Header styles */
    h1, h2, h3, h4, h5, h6 {
        color: var(--dark) !important;
        font-weight: 700 !important;
    }
    
    /* Button styles */
    .stButton>button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Input fields */
    .stTextInput>div>div>input, 
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 8px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        padding: 0 20px;
        border-radius: 8px !important;
        background-color: #edf2f7 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary) !important;
        color: white !important;
    }
    
    /* Metric cards */
    [data-testid="metric-container"] {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border-radius: 12px;
        padding: 20px;
        background: white;
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* Login animation */
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary);
    }
    
    /* Custom hr style */
    .stMarkdown hr {
        height: 2px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        border: none;
        margin: 1.5rem 0;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        color: var(--dark) !important;
    }
    
    /* Custom select box arrow */
    .stSelectbox:after {
        color: var(--primary) !important;
    }
    
    /* Custom radio buttons */
    .stRadio [role="radiogroup"] {
        gap: 15px;
    }
    
    .stRadio [class*="st-"] {
        padding: 8px 15px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stRadio [class*="st-"]:hover {
        border-color: var(--primary);
    }
    
    .stRadio [aria-checked="true"] {
        background-color: rgba(110, 142, 251, 0.1) !important;
        border-color: var(--primary) !important;
        color: var(--primary) !important;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# Database connection function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='552005',
            database='field_training2'
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Initialize session state for user authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# Modern gradient button style
def gradient_button(text, key=None):
    button_style = """
    <style>
    .gradient-button {
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .gradient-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    return st.button(text, key=key)

# Modern login page with animated gradient background
def login_page():
    st.set_page_config(layout="wide", page_title="Field Training System", page_icon="🎓")
    
    # Apply custom CSS
    local_css()
    
    # Center the login form
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with stylable_container(
            key="login_container",
            css_styles="""
                {
                    background: rgba(255, 255, 255, 0.9);
                    border-radius: 15px;
                    padding: 2rem;
                    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
                    backdrop-filter: blur(8px);
                    border: 1px solid rgba(255, 255, 255, 0.18);
                }
            """
        ):
            st.markdown("""
            <h1 style='text-align: center; color: #4a4a4a; margin-bottom: 1.5rem;'>
                <span style="background: linear-gradient(135deg, #6e8efb, #a777e3); 
                -webkit-background-clip: text; background-clip: text; color: transparent;">
                    Field Training System
                </span>
            </h1>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                st.markdown("<h3 style='text-align: center; margin-bottom: 1.5rem;'>Login</h3>", unsafe_allow_html=True)
                
                user_id = st.number_input("👤 User ID", min_value=1, step=1, key="login_id")
                role = st.selectbox("🎭 Role", ["Student", "Company Mentor", "University Coordinator"], key="login_role")
                
                submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
                
                if submitted:
                    conn = create_connection()
                    if conn:
                        cursor = conn.cursor()
                        
                        # Verify user exists and role matches
                        if role == "Student":
                            cursor.execute("SELECT Student_ID FROM Student WHERE Student_ID = %s", (user_id,))
                        elif role == "Company Mentor":
                            cursor.execute("SELECT Company_Mentor_ID FROM Company_Mentor WHERE Company_Mentor_ID = %s", (user_id,))
                        else:  # University Coordinator
                            cursor.execute("SELECT Uni_Mentor_ID FROM Uni_Mentor WHERE Uni_Mentor_ID = %s", (user_id,))
                        
                        result = cursor.fetchone()
                        conn.close()
                        
                        if result:
                            st.session_state.authenticated = True
                            st.session_state.user_role = role
                            st.session_state.user_id = user_id
                            st.rerun()
                        else:
                            st.error("Invalid credentials or role mismatch")

# Modern student dashboard with sleek UI
def student_dashboard():
    st.set_page_config(layout="wide", page_title="Student Dashboard", page_icon="🎓")
    local_css()
    
    # Sidebar with user info
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #6e8efb, #a777e3); 
                    border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h3>Student Profile</h3>
            <p style="font-size: 1.2rem; font-weight: 600;">ID: {st.session_state.user_id}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True, type="primary"):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.user_id = None
            st.rerun()
    
    # Main content
    st.markdown("""
    <h1 style="display: flex; align-items: center; gap: 0.5rem;">
        <span style="background: linear-gradient(135deg, #6e8efb, #a777e3); 
        -webkit-background-clip: text; background-clip: text; color: transparent;">
            Student Dashboard
        </span>
        🎓
    </h1>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Student Information
        cursor.execute("""
            SELECT s.*, u.Name, u.Phone_No, u.Email, u.Address 
            FROM Student s JOIN User u ON s.Student_ID = u.ID 
            WHERE s.Student_ID = %s
        """, (st.session_state.user_id,))
        student_info = cursor.fetchone()
        
        if student_info:
            with stylable_container(
                key="info_box",
                css_styles="""
                    {
                        background: white;
                        border-radius: 12px;
                        padding: 1.5rem;
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                        margin-bottom: 1.5rem;
                    }
                """
            ):
                st.subheader("👤 Personal Information")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Name:** {student_info['Name']}")
                    st.markdown(f"**Major:** {student_info['Major']}")
                with col2:
                    st.markdown(f"**Academic Level:** {student_info['Academic_Level']}")
                    st.markdown(f"**CGPA:** {student_info['CGPA']}")
                with col3:
                    status_color = "#48bb78" if student_info['Application_State'] == "Approved" else "#ed8936" if student_info['Application_State'] == "Pending" else "#f56565"
                    st.markdown(f"**Application State:** <span style='color: {status_color}; font-weight: 600;'>{student_info['Application_State']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Email:** {student_info['Email']}")
            
            st.markdown("---")
            
            # Internship Applications
            st.subheader("📝 Internship Applications")
            cursor.execute("""
                SELECT ia.Application_ID, ia.Status, ia.Applied_Date, ia.Decision_Date,
                       c.Name AS Company_Name, c.Industry, 
                       um.Uni_Name AS University_Mentor,
                       cm.Company_Name AS Company_Mentor
                FROM Internship_Application ia
                LEFT JOIN Company_Mentor cm ON ia.Company_Mentor_ID = cm.Company_Mentor_ID
                LEFT JOIN Has_a_Relation hr ON ia.Application_ID = hr.Application_ID
                LEFT JOIN Company c ON hr.Company_Logo = c.Company_Logo
                LEFT JOIN Uni_Mentor um ON ia.Uni_Mentor_ID = um.Uni_Mentor_ID
                WHERE ia.Student_ID = %s
            """, (st.session_state.user_id,))
            applications = cursor.fetchall()
            
            if applications:
                df = pd.DataFrame(applications)
                df['Status'] = df['Status'].apply(lambda x: f"🟢 {x}" if x == "Accepted" else f"🟡 {x}" if x == "Pending" else f"🔴 {x}")
                
                # Use tabs for different views
                tab1, tab2 = st.tabs(["📋 Table View", "📊 Visualization"])
                
                with tab1:
                    st.dataframe(df, hide_index=True, use_container_width=True)
                
                with tab2:
                    status_counts = df['Status'].value_counts().reset_index()
                    status_counts.columns = ['Status', 'Count']
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        fig = px.pie(status_counts, values='Count', names='Status', 
                                    title='Application Status Distribution',
                                    color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        fig = px.bar(status_counts, x='Status', y='Count', 
                                    title='Application Status Count',
                                    color='Status',
                                    color_discrete_sequence=px.colors.qualitative.Pastel)
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No internship applications found")
            
            st.markdown("---")
            
            # Evaluation Reports
            st.subheader("📊 Evaluation Reports")
            cursor.execute("""
                SELECT er.Report_ID, er.Evaluation_Date, er.Performance_Score, er.Feedback,
                       c.Name AS Company_Name, cm.Company_Name AS Mentor_Name
                FROM Evaluation_Report er
                JOIN Company_Mentor cm ON er.Company_Mentor_ID = cm.Company_Mentor_ID
                JOIN Internship_Application ia ON cm.Company_Mentor_ID = ia.Company_Mentor_ID
                JOIN Has_a_Relation hr ON ia.Application_ID = hr.Application_ID
                JOIN Company c ON hr.Company_Logo = c.Company_Logo
                WHERE ia.Student_ID = %s
            """, (st.session_state.user_id,))
            evaluations = cursor.fetchall()
            
            if evaluations:
                df = pd.DataFrame(evaluations)
                
                # Display metrics
                avg_score = df['Performance_Score'].mean()
                latest_eval = df.iloc[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    with stylable_container(
                        key="avg_score",
                        css_styles="""
                            {
                                background: white;
                                border-radius: 12px;
                                padding: 1rem;
                                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                            }
                        """
                    ):
                        st.metric("Average Performance Score", f"{avg_score:.1f}/5.0", 
                                 delta_color="off")
                
                with col2:
                    with stylable_container(
                        key="latest_eval",
                        css_styles="""
                            {
                                background: white;
                                border-radius: 12px;
                                padding: 1rem;
                                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                            }
                        """
                    ):
                        st.metric("Latest Evaluation", f"{latest_eval['Performance_Score']}/5.0", 
                                 f"by {latest_eval['Mentor_Name']}")
                
                # Show feedback
                with st.expander("💬 View Latest Feedback", expanded=False):
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px;">
                        {latest_eval['Feedback']}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Show all evaluations
                st.dataframe(df, hide_index=True, use_container_width=True)
                
                # Performance trend chart
                df['Evaluation_Date'] = pd.to_datetime(df['Evaluation_Date'])
                df = df.sort_values('Evaluation_Date')
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df['Evaluation_Date'],
                    y=df['Performance_Score'],
                    mode='lines+markers',
                    name='Performance Score',
                    line=dict(color='#6e8efb', width=3),
                    marker=dict(size=8, color='#a777e3')
                ))
                
                fig.update_layout(
                    title='Performance Trend Over Time',
                    xaxis_title='Evaluation Date',
                    yaxis_title='Score (out of 5)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    yaxis=dict(range=[0, 5.5])
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No evaluation reports found")
            
            st.markdown("---")
            
            # Document Upload
            st.subheader("📤 Document Upload")
            with stylable_container(
                key="doc_upload",
                css_styles="""
                    {
                        background: white;
                        border-radius: 12px;
                        padding: 1rem;
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                    }
                """
            ):
                with st.expander("📎 Upload Documents", expanded=False):
                    with st.form("document_upload"):
                        doc_type = st.selectbox("Document Type", ["Transcript", "Recommendation Letter"])
                        uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx'])
                        submitted = st.form_submit_button("Upload", type="primary")
                        
                        if submitted and uploaded_file:
                            try:
                                # Get next Doc_ID
                                cursor.execute("SELECT MAX(Doc_ID) FROM Academic_Docs")
                                max_id = cursor.fetchone()['MAX(Doc_ID)'] or 0
                                new_id = max_id + 1
                                
                                # Get Uni_Mentor_ID
                                cursor.execute("SELECT Uni_Mentor_ID FROM Student WHERE Student_ID = %s", (st.session_state.user_id,))
                                uni_mentor_id = cursor.fetchone()['Uni_Mentor_ID']
                                
                                # Insert document
                                cursor.execute("""
                                    INSERT INTO Academic_Docs (Doc_ID, Uploaded_By, Uni_Mentor_ID, Timestamp, 
                                                             Transcript, Recommendation_Letter)
                                    VALUES (%s, %s, %s, %s, %s, %s)
                                """, (
                                    new_id,
                                    student_info['Name'],
                                    uni_mentor_id,
                                    datetime.datetime.now(),
                                    uploaded_file.read() if doc_type == "Transcript" else None,
                                    uploaded_file.read() if doc_type == "Recommendation Letter" else None
                                ))
                                conn.commit()
                                st.toast("✅ Document uploaded successfully!", icon=None)
                            except Error as e:
                                st.error(f"Error uploading document: {e}")
            
            st.markdown("---")
            
            # Application Form
            st.subheader("➕ New Internship Application")
            with stylable_container(
                key="new_app",
                css_styles="""
                    {
                        background: white;
                        border-radius: 12px;
                        padding: 1rem;
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                    }
                """
            ):
                with st.expander("📝 Create New Application", expanded=False):
                    with st.form("new_application"):
                        cursor.execute("SELECT Company_Logo, Name FROM Company")
                        companies = cursor.fetchall()
                        company_options = {c['Name']: c['Company_Logo'] for c in companies}
                        selected_company = st.selectbox("Company", list(company_options.keys()))
                        
                        cursor.execute("""
                            SELECT cm.Company_Mentor_ID, cm.Company_Name, u.Name 
                            FROM Company_Mentor cm JOIN User u ON cm.Mentor_ID = u.ID
                            WHERE cm.Company_Logo = %s
                        """, (company_options[selected_company],))
                        mentors = cursor.fetchall()
                        mentor_options = {f"{m['Name']} ({m['Company_Name']})": m['Company_Mentor_ID'] for m in mentors}
                        selected_mentor = st.selectbox("Company Mentor", list(mentor_options.keys()))
                        
                        cursor.execute("SELECT Doc_ID FROM Academic_Docs WHERE Uploaded_By = %s", (student_info['Name'],))
                        docs = cursor.fetchall()
                        doc_options = {d['Doc_ID']: d['Doc_ID'] for d in docs}
                        selected_doc = st.selectbox("Select Document", list(doc_options.keys()))
                        
                        submitted = st.form_submit_button("Submit Application", type="primary")
                        
                        if submitted:
                            try:
                                # Get next Application_ID
                                cursor.execute("SELECT MAX(Application_ID) FROM Internship_Application")
                                max_id = cursor.fetchone()['MAX(Application_ID)'] or 0
                                new_id = max_id + 1
                                
                                # Get Uni_Mentor_ID
                                cursor.execute("SELECT Uni_Mentor_ID FROM Student WHERE Student_ID = %s", (st.session_state.user_id,))
                                uni_mentor_id = cursor.fetchone()['Uni_Mentor_ID']
                                
                                # Insert application
                                cursor.execute("""
                                    INSERT INTO Internship_Application 
                                    (Application_ID, Company_Mentor_ID, Uni_Mentor_ID, Student_ID, 
                                     Status, Applied_Date, Doc_ID)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """, (
                                    new_id,
                                    mentor_options[selected_mentor],
                                    uni_mentor_id,
                                    st.session_state.user_id,
                                    'Pending',
                                    datetime.date.today(),
                                    selected_doc
                                ))
                                
                                # Insert into Has_a_Relation
                                cursor.execute("""
                                    INSERT INTO Has_a_Relation (Company_Logo, Application_ID)
                                    VALUES (%s, %s)
                                """, (company_options[selected_company], new_id))
                                
                                conn.commit()
                                st.toast("✅ Application submitted successfully!", icon=None)
                            except Error as e:
                                st.error(f"Error submitting application: {e}")
            
            st.markdown("---")
            
            # Export Reports
            st.subheader("📥 Export Data")
            with stylable_container(
                key="export_data",
                css_styles="""
                    {
                        background: white;
                        border-radius: 12px;
                        padding: 1rem;
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                    }
                """
            ):
                with st.expander("💾 Export Options", expanded=False):
                    if st.button("Export My Information", use_container_width=True):
                        cursor.execute("SELECT * FROM Student WHERE Student_ID = %s", (st.session_state.user_id,))
                        student_data = cursor.fetchone()
                        df = pd.DataFrame([student_data])
                        
                        # Convert to CSV
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download as CSV",
                            data=csv,
                            file_name=f"student_{st.session_state.user_id}_info.csv",
                            mime='text/csv',
                            use_container_width=True
                        )
        
        conn.close()

# Modern company mentor dashboard with sleek UI
def company_mentor_dashboard():
    st.set_page_config(layout="wide", page_title="Mentor Dashboard", page_icon="👔")
    local_css()
    
    # Sidebar with user info
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #6e8efb, #a777e3); 
                    border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h3>Mentor Profile</h3>
            <p style="font-size: 1.2rem; font-weight: 600;">ID: {st.session_state.user_id}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True, type="primary"):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.user_id = None
            st.rerun()
    
    # Main content
    st.markdown("""
    <h1 style="display: flex; align-items: center; gap: 0.5rem;">
        <span style="background: linear-gradient(135deg, #6e8efb, #a777e3); 
        -webkit-background-clip: text; background-clip: text; color: transparent;">
            Company Mentor Dashboard
        </span>
        👔
    </h1>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    conn = create_connection()
    if not conn:
        st.error("Could not connect to database.")
        return

    cursor = conn.cursor(dictionary=True)
    
    # 1) Mentor Information
    cursor.execute("""
        SELECT
            cm.Company_Mentor_ID,
            mentor_u.Name    AS Mentor_Name,
            mentor_u.Phone_No,
            mentor_u.Email,
            mentor_u.Address,
            c.Name           AS Company_Name,
            cm.Assigned_Branch
        FROM Company_Mentor cm 
        JOIN User AS mentor_u
          ON cm.Mentor_ID = mentor_u.ID
        JOIN Company c
          ON cm.Company_Logo = c.Company_Logo
        WHERE cm.Company_Mentor_ID = %s
    """, (st.session_state.user_id,))
    mentor_info = cursor.fetchone()
    
    if not mentor_info:
        st.warning("No such mentor found.")
        conn.close()
        return

    with stylable_container(
        key="mentor_info",
        css_styles="""
            {
                background: white;
                border-radius: 12px;
                padding: 1.5rem;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                margin-bottom: 1.5rem;
            }
        """
    ):
        st.subheader("👤 Personal Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Name:** {mentor_info['Mentor_Name']}")
            st.markdown(f"**Company:** {mentor_info['Company_Name']}")
        with col2:
            st.markdown(f"**Assigned Branch:** {mentor_info['Assigned_Branch']}")
            st.markdown(f"**Email:** {mentor_info['Email']}")
        with col3:
            st.markdown(f"**Phone:** {mentor_info['Phone_No']}")
            st.markdown(f"**Address:** {mentor_info['Address']}")
    
    st.markdown("---")
    
    # 2) Assigned Students
    st.subheader("🎓 Assigned Students")
    cursor.execute("""
        SELECT
            s.Student_ID,
            student_u.Name         AS Student_Name,
            s.Major,
            s.CGPA,
            s.Academic_Level,
            ia.Application_ID,
            ia.Status,
            ia.Applied_Date
        FROM Internship_Application ia
        JOIN Student s
          ON ia.Student_ID = s.Student_ID
        JOIN User AS student_u
          ON s.Student_ID = student_u.ID
        WHERE ia.Company_Mentor_ID = %s
    """, (st.session_state.user_id,))
    students = pd.DataFrame(cursor.fetchall())

    if students.empty:
        st.info("No students assigned to you.")
    else:
        # Metrics row
        col1, col2, col3 = st.columns(3)
        with col1:
            with stylable_container(
                key="total_students",
                css_styles="""
                    {
                        background: white;
                        border-radius: 12px;
                        padding: 1rem;
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                    }
                """
            ):
                st.metric("Total Students", len(students))
        
        with col2:
            with stylable_container(
                key="avg_cgpa",
                css_styles="""
                    {
                        background: white;
                        border-radius: 12px;
                        padding: 1rem;
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                    }
                """
            ):
                st.metric("Average CGPA", f"{students['CGPA'].mean():.2f}")
        
        with col3:
            with stylable_container(
                key="placement_rate",
                css_styles="""
                    {
                        background: white;
                        border-radius: 12px;
                        padding: 1rem;
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                    }
                """
            ):
                placement_rate = (students['Status'] == 'Accepted').mean() * 100
                st.metric("Placement Rate", f"{placement_rate:.1f}%")
        
        # Display students
        tab1, tab2 = st.tabs(["📋 Table View", "📊 Performance Analysis"])
        
        with tab1:
            st.dataframe(students, hide_index=True, use_container_width=True)
        
        with tab2:
            # Get performance data for visualization
            cursor.execute("""
                SELECT 
                    s.Student_ID,
                    student_u.Name AS Student_Name,
                    AVG(ps.Score) AS Avg_Score
                FROM Performance_Score ps
                JOIN Evaluation_Report er ON ps.Report_ID = er.Report_ID
                JOIN Student s ON ps.Student_ID = s.Student_ID
                JOIN User AS student_u ON s.Student_ID = student_u.ID
                WHERE er.Company_Mentor_ID = %s
                GROUP BY s.Student_ID, student_u.Name
            """, (st.session_state.user_id,))
            performance = pd.DataFrame(cursor.fetchall())
            
            if not performance.empty:
                col1, col2 = st.columns(2)
                with col1:
                    fig = px.bar(performance, x='Student_Name', y='Avg_Score', 
                                title='Student Performance Scores',
                                color='Avg_Score',
                                color_continuous_scale='Bluered')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = px.pie(performance, values='Avg_Score', names='Student_Name', 
                                title='Performance Distribution',
                                hole=0.4)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No performance data available")
        
        st.markdown("---")
        
        # Student evaluation form
        st.subheader("📝 Student Evaluation")
        with stylable_container(
            key="eval_form",
            css_styles="""
                {
                    background: white;
                    border-radius: 12px;
                    padding: 1rem;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                }
            """
        ):
            with st.expander("✏️ Evaluate Student", expanded=False):
                options = [f"{row['Student_ID']} – {row['Student_Name']}" for _, row in students.iterrows()]
                selected = st.selectbox("Select Student", options)
                selected_id = int(selected.split(" – ")[0])

                with st.form("student_evaluation"):
                    col1, col2 = st.columns(2)
                    with col1:
                        performance_score = st.slider("Performance Score", 1.0, 5.0, 3.0, 0.1)
                        evaluation_date = st.date_input("Evaluation Date", datetime.date.today())
                    with col2:
                        feedback = st.text_area("Feedback", height=150)
                    
                    submitted = st.form_submit_button("Submit Evaluation", type="primary")

                    if submitted:
                        try:
                            cursor.execute("SELECT MAX(Report_ID) AS max_id FROM Evaluation_Report")
                            max_id = cursor.fetchone()['max_id'] or 0
                            new_id = max_id + 1

                            cursor.execute("""
                                INSERT INTO Evaluation_Report
                                    (Report_ID, Evaluation_Date, Company_Mentor_ID, Performance_Score, Feedback)
                                VALUES (%s, %s, %s, %s, %s)
                            """, (new_id, evaluation_date, st.session_state.user_id, performance_score, feedback))

                            cursor.execute("""
                                INSERT INTO Performance_Score
                                    (Report_ID, Student_ID, Score)
                                VALUES (%s, %s, %s)
                            """, (new_id, selected_id, performance_score))

                            conn.commit()
                            st.toast("✅ Evaluation submitted successfully!", icon=None)
                        except Error as e:
                            st.error(f"Error submitting evaluation: {e}")
        
        st.markdown("---")
        
        # Reports
        st.subheader("📊 Generate Reports")
        with stylable_container(
            key="reports",
            css_styles="""
                {
                    background: white;
                    border-radius: 12px;
                    padding: 1rem;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                }
            """
        ):
            with st.expander("📈 Report Options", expanded=False):
                report_type = st.selectbox("Report Type", ["Student Performance", "Application Status"])
                
                if st.button("Generate Report", use_container_width=True, type="primary"):
                    if report_type == "Student Performance":
                        cursor.execute("""
                            SELECT s.Student_ID, u.Name, ps.Score, er.Evaluation_Date, er.Feedback
                            FROM Performance_Score ps
                            JOIN Evaluation_Report er ON ps.Report_ID = er.Report_ID
                            JOIN Student s ON ps.Student_ID = s.Student_ID
                            JOIN User u ON s.Student_ID = u.ID
                            WHERE er.Company_Mentor_ID = %s
                        """, (st.session_state.user_id,))
                    else:  # Application Status
                        cursor.execute("""
                            SELECT ia.Application_ID, s.Student_ID, u.Name, ia.Status, 
                                   ia.Applied_Date, ia.Decision_Date
                            FROM Internship_Application ia
                            JOIN Student s ON ia.Student_ID = s.Student_ID
                            JOIN User u ON s.Student_ID = u.ID
                            WHERE ia.Company_Mentor_ID = %s
                        """, (st.session_state.user_id,))
                    
                    report_data = pd.DataFrame(cursor.fetchall())
                    if not report_data.empty:
                        st.dataframe(report_data, hide_index=True, use_container_width=True)
                        
                        # Export options
                        export_format = st.selectbox("Export Format", ["CSV", "Excel"])
                        
                        if export_format == "CSV":
                            csv = report_data.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label="Download CSV",
                                data=csv,
                                file_name=f"{report_type.replace(' ', '_')}_report.csv",
                                mime='text/csv',
                                use_container_width=True
                            )
                        else:  # Excel
                            output = BytesIO()
                            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                                report_data.to_excel(writer, index=False, sheet_name='Report')
                            excel_data = output.getvalue()
                            st.download_button(
                                label="Download Excel",
                                data=excel_data,
                                file_name=f"{report_type.replace(' ', '_')}_report.xlsx",
                                mime='application/vnd.ms-excel',
                                use_container_width=True
                            )
                    else:
                        st.info("No data available for this report")
    
    conn.close()

# Modern university coordinator dashboard with sleek UI
def university_coordinator_dashboard():
    st.set_page_config(layout="wide", page_title="Coordinator Dashboard", page_icon="🏫")
    local_css()
    
    # Sidebar with user info
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #6e8efb, #a777e3); 
                    border-radius: 12px; color: white; margin-bottom: 1.5rem;">
            <h3>Coordinator Profile</h3>
            <p style="font-size: 1.2rem; font-weight: 600;">ID: {st.session_state.user_id}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True, type="primary"):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.user_id = None
            st.rerun()
    
    # Main content
    st.markdown("""
    <h1 style="display: flex; align-items: center; gap: 0.5rem;">
        <span style="background: linear-gradient(135deg, #6e8efb, #a777e3); 
        -webkit-background-clip: text; background-clip: text; color: transparent;">
            University Coordinator Dashboard
        </span>
        🏫
    </h1>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Coordinator Information
        cursor.execute("""
            SELECT um.*, u.Name, u.Phone_No, u.Email, u.Address
            FROM Uni_Mentor um
            JOIN User u ON um.Uni_Mentor_ID = u.ID
            WHERE um.Uni_Mentor_ID = %s
        """, (st.session_state.user_id,))
        coordinator_info = cursor.fetchone()
        
        if coordinator_info:
            with stylable_container(
                key="coord_info",
                css_styles="""
                    {
                        background: white;
                        border-radius: 12px;
                        padding: 1.5rem;
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                        margin-bottom: 1.5rem;
                    }
                """
            ):
                st.subheader("👤 Personal Information")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Name:** {coordinator_info['Name']}")
                    st.markdown(f"**University:** {coordinator_info['Uni_Name']}")
                with col2:
                    st.markdown(f"**Department:** {coordinator_info['Department']}")
                    st.markdown(f"**Job Title:** {coordinator_info['Job_Title']}")
                with col3:
                    st.markdown(f"**Feedback Score:** {coordinator_info['Feedback_Score']}")
                    st.markdown(f"**Email:** {coordinator_info['Email']}")
            
            st.markdown("---")
            
            # Assigned Students
            st.subheader("🎓 Assigned Students")
            cursor.execute("""
                SELECT s.Student_ID, u.Name, s.Major, s.CGPA, s.Academic_Level,
                       s.Application_State, ia.Status AS Internship_Status,
                       c.Name AS Company_Name, cm.Company_Name AS Mentor_Name
                FROM Student s
                JOIN User u ON s.Student_ID = u.ID
                LEFT JOIN Internship_Application ia ON s.Student_ID = ia.Student_ID
                LEFT JOIN Has_a_Relation hr ON ia.Application_ID = hr.Application_ID
                LEFT JOIN Company c ON hr.Company_Logo = c.Company_Logo
                LEFT JOIN Company_Mentor cm ON ia.Company_Mentor_ID = cm.Company_Mentor_ID
                WHERE s.Uni_Mentor_ID = %s
            """, (st.session_state.user_id,))
            students = pd.DataFrame(cursor.fetchall())
            
            if not students.empty:
                # Metrics row
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    with stylable_container(
                        key="total_students",
                        css_styles="""
                            {
                                background: white;
                                border-radius: 12px;
                                padding: 1rem;
                                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                            }
                        """
                    ):
                        st.metric("Total Students", len(students))
                
                with col2:
                    with stylable_container(
                        key="avg_cgpa",
                        css_styles="""
                            {
                                background: white;
                                border-radius: 12px;
                                padding: 1rem;
                                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                            }
                        """
                    ):
                        st.metric("Average CGPA", f"{students['CGPA'].mean():.2f}")
                
                with col3:
                    with stylable_container(
                        key="placed_students",
                        css_styles="""
                            {
                                background: white;
                                border-radius: 12px;
                                padding: 1rem;
                                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                            }
                        """
                    ):
                        placed = (students['Internship_Status'] == 'Accepted').sum()
                        st.metric("Placed Students", f"{placed}/{len(students)}")
                
                with col4:
                    with stylable_container(
                        key="placement_rate",
                        css_styles="""
                            {
                                background: white;
                                border-radius: 12px;
                                padding: 1rem;
                                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                            }
                        """
                    ):
                        placement_rate = (placed/len(students))*100 if len(students) > 0 else 0
                        st.metric("Placement Rate", f"{placement_rate:.1f}%")
                
                # Display students
                tab1, tab2 = st.tabs(["📋 Table View", "📊 Placement Analysis"])
                
                with tab1:
                    st.dataframe(students, hide_index=True, use_container_width=True)
                
                with tab2:
                    if 'Internship_Status' in students.columns:
                        status_counts = students['Internship_Status'].value_counts().reset_index()
                        status_counts.columns = ['Status', 'Count']
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            fig = px.pie(status_counts, values='Count', names='Status', 
                                        title='Student Placement Status',
                                        hole=0.4,
                                        color_discrete_sequence=px.colors.qualitative.Pastel)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            fig = px.bar(status_counts, x='Status', y='Count',
                                        title='Placement Count by Status',
                                        color='Status',
                                        color_discrete_sequence=px.colors.qualitative.Pastel)
                            st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No students assigned to you")
            
            st.markdown("---")
            
            # Statistics
            st.subheader("📈 Statistics")
            cursor.execute("""
                SELECT 
                    COUNT(*) AS Total_Students,
                    AVG(s.CGPA) AS Avg_CGPA,
                    COUNT(CASE WHEN ia.Status = 'Accepted' THEN 1 END) AS Placed_Students,
                    COUNT(DISTINCT c.Company_Logo) AS Partner_Companies,
                    AVG(er.Performance_Score) AS Avg_Performance
                FROM Student s
                LEFT JOIN Internship_Application ia ON s.Student_ID = ia.Student_ID
                LEFT JOIN Has_a_Relation hr ON ia.Application_ID = hr.Application_ID
                LEFT JOIN Company c ON hr.Company_Logo = c.Company_Logo
                LEFT JOIN Evaluation_Report er ON ia.Company_Mentor_ID = er.Company_Mentor_ID
                WHERE s.Uni_Mentor_ID = %s
            """, (st.session_state.user_id,))
            stats = cursor.fetchone()
            
            if stats:
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    with stylable_container(
                        key="total_students",
                        css_styles="""
                            {
                                background: white;
                                border-radius: 12px;
                                padding: 1rem;
                                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                            }
                        """
                    ):
                        st.metric("Total Students", stats['Total_Students'])
                
                with col2:
                    with stylable_container(
                        key="avg_cgpa",
                        css_styles="""
                            {
                                background: white;
                                border-radius: 12px;
                                padding: 1rem;
                                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                            }
                        """
                    ):
                        st.metric("Avg CGPA", f"{stats['Avg_CGPA']:.2f}")
                
                with col3:
                    with stylable_container(
                        key="placed_students",
                        css_styles="""
                            {
                                background: white;
                                border-radius: 12px;
                                padding: 1rem;
                                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                            }
                        """
                    ):
                        st.metric("Placed", stats['Placed_Students'])
                
                with col4:
                    with stylable_container(
                        key="partner_companies",
                        css_styles="""
                            {
                                background: white;
                                border-radius: 12px;
                                padding: 1rem;
                                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                            }
                        """
                    ):
                        st.metric("Companies", stats['Partner_Companies'])
                
                with col5:
                    with stylable_container(
                        key="avg_performance",
                        css_styles="""
                            {
                                background: white;
                                border-radius: 12px;
                                padding: 1rem;
                                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                            }
                        """
                    ):
                        st.metric("Avg Performance", f"{stats['Avg_Performance']:.2f}" if stats['Avg_Performance'] else "N/A")
            
            st.markdown("---")
            
            # Document Management
            st.subheader("📂 Document Management")
            cursor.execute("""
                SELECT ad.Doc_ID, ad.Uploaded_By, ad.Timestamp, 
                       ad.Transcript IS NOT NULL AS Has_Transcript,
                       ad.Recommendation_Letter IS NOT NULL AS Has_Recommendation
                FROM Academic_Docs ad
                WHERE ad.Uni_Mentor_ID = %s
            """, (st.session_state.user_id,))
            docs = pd.DataFrame(cursor.fetchall())
            
            if not docs.empty:
                with stylable_container(
                    key="doc_table",
                    css_styles="""
                        {
                            background: white;
                            border-radius: 12px;
                            padding: 1rem;
                            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                            margin-bottom: 1.5rem;
                        }
                    """
                ):
                    st.dataframe(docs, hide_index=True, use_container_width=True)
                
                # Document selection for download
                with stylable_container(
                    key="doc_download",
                    css_styles="""
                        {
                            background: white;
                            border-radius: 12px;
                            padding: 1rem;
                            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                        }
                    """
                ):
                    selected_doc = st.selectbox("Select Document to Download", 
                                              [f"{d['Doc_ID']} - {d['Uploaded_By']}" for _, d in docs.iterrows()])
                    selected_id = int(selected_doc.split(" - ")[0])
                    
                    doc_type = st.radio("Document Type", ["Transcript", "Recommendation Letter"])
                    
                    if st.button("Download Document", use_container_width=True, type="primary"):
                        cursor.execute("""
                            SELECT %s FROM Academic_Docs WHERE Doc_ID = %s
                        """ % ("Transcript" if doc_type == "Transcript" else "Recommendation_Letter", selected_id))
                        doc_content = cursor.fetchone()
                        
                        if doc_content and doc_content[doc_type.lower().replace(' ', '_')]:
                            st.download_button(
                                label=f"Download {doc_type}",
                                data=doc_content[doc_type.lower().replace(' ', '_')],
                                file_name=f"{doc_type.lower()}_{selected_id}.pdf",
                                mime='application/pdf',
                                use_container_width=True
                            )
                        else:
                            st.warning("Document not found")
            else:
                st.info("No documents available")
            
            st.markdown("---")
            
            # Reports
            st.subheader("📊 Generate Reports")
            with stylable_container(
                key="reports",
                css_styles="""
                    {
                        background: white;
                        border-radius: 12px;
                        padding: 1rem;
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                    }
                """
            ):
                with st.expander("📈 Report Options", expanded=False):
                    report_type = st.selectbox("Report Type", ["Student Placement", "Company Statistics"])
                    
                    if st.button("Generate Report", use_container_width=True, type="primary"):
                        if report_type == "Student Placement":
                            cursor.execute("""
                                SELECT s.Student_ID, u.Name, s.Major, s.CGPA, 
                                       ia.Status AS Internship_Status, c.Name AS Company_Name,
                                       er.Performance_Score
                                FROM Student s
                                JOIN User u ON s.Student_ID = u.ID
                                LEFT JOIN Internship_Application ia ON s.Student_ID = ia.Student_ID
                                LEFT JOIN Has_a_Relation hr ON ia.Application_ID = hr.Application_ID
                                LEFT JOIN Company c ON hr.Company_Logo = c.Company_Logo
                                LEFT JOIN Evaluation_Report er ON ia.Company_Mentor_ID = er.Company_Mentor_ID
                                WHERE s.Uni_Mentor_ID = %s
                            """, (st.session_state.user_id,))
                        else:  # Company Statistics
                            cursor.execute("""
                                SELECT c.Name, c.Industry, 
                                       COUNT(DISTINCT ia.Student_ID) AS Num_Students,
                                       AVG(er.Performance_Score) AS Avg_Performance
                                FROM Company c
                                JOIN Has_a_Relation hr ON c.Company_Logo = hr.Company_Logo
                                JOIN Internship_Application ia ON hr.Application_ID = ia.Application_ID
                                LEFT JOIN Evaluation_Report er ON ia.Company_Mentor_ID = er.Company_Mentor_ID
                                WHERE ia.Uni_Mentor_ID = %s
                                GROUP BY c.Name, c.Industry
                            """, (st.session_state.user_id,))
                        
                        report_data = pd.DataFrame(cursor.fetchall())
                        if not report_data.empty:
                            st.dataframe(report_data, hide_index=True, use_container_width=True)
                            
                            # Export options
                            export_format = st.selectbox("Format", ["CSV", "Excel"])
                            
                            if export_format == "CSV":
                                csv = report_data.to_csv(index=False).encode('utf-8')
                                st.download_button(
                                    label="Download CSV",
                                    data=csv,
                                    file_name=f"{report_type.replace(' ', '_')}_report.csv",
                                    mime='text/csv',
                                    use_container_width=True
                                )
                            else:  # Excel
                                output = BytesIO()
                                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                                    report_data.to_excel(writer, index=False, sheet_name='Report')
                                excel_data = output.getvalue()
                                st.download_button(
                                    label="Download Excel",
                                    data=excel_data,
                                    file_name=f"{report_type.replace(' ', '_')}_report.xlsx",
                                    mime='application/vnd.ms-excel',
                                    use_container_width=True
                                )
                        else:
                            st.info("No data available for this report")
        
        conn.close()

# Main App
def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        # Role-based dashboard
        if st.session_state.user_role == "Student":
            student_dashboard()
        elif st.session_state.user_role == "Company Mentor":
            company_mentor_dashboard()
        elif st.session_state.user_role == "University Coordinator":
            university_coordinator_dashboard()

if __name__ == "__main__":
    main()