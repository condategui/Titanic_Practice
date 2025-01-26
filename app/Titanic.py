# Import libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import os
from streamlit_option_menu import option_menu

#-----------------------------------------------------------------------------------------------------

# Import icons
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space

#-----------------------------------------------------------------------------------------------------

# Load data
df = pd.read_csv(r'streamlitenv/data/Titanic_check.csv')

#-----------------------------------------------------------------------------------------------------

# Add a custom blue theme
def set_blue_theme():
    st.markdown("""
    <style>
    .stApp {
        background-color: #0B1354;  /* Deep Navy Blue */
        color: #E6E6FA;  /* Lavender for text */
    }
    .stButton>button {
        background-color: #1E456E;  /* Dark Blue */
        color: #E6E6FA;
    }
    .stSidebar {
        background-color: #13315C;  /* Darker Blue */
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0B1354;  /* Match main background */
    }
    .stTabs [data-baseweb="tab"] {
        color: #E6E6FA;
    }
    /* Ensure text is readable */
    .stMarkdown, .stDataFrame, .stText {
        color: #E6E6FA;
    }
    /* Chart and plot adjustments */
    .stPlotlyChart {
        background-color: #13315C;
    }
    </style>
    """, unsafe_allow_html=True)

# Utility functions for charts
def count_plot(df, x, hue=None, title='', palette='Blues_d'):
    plt.figure(figsize=(10, 6), facecolor='black')
    plt.rcParams['text.color'] = 'white'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'
    sns.countplot(
        data=df,
        x=x,
        hue=hue,
        palette=palette,
        width=0.8,
        dodge=False
    )
    plt.title(title, color='white')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt.gcf()

def bar_chart(data, x, y, title=''):
    fig = px.bar(data, x=x, y=y, title=title)
    return fig


def pie_chart(data, names, values, title='', color_palette="Blues_d"):
    # Generate the color palette based on the provided palette name and the number of values
    colors = sns.color_palette(color_palette, len(data[names].unique())).as_hex()
    
    # Create the pie chart
    fig = px.pie(
        data, 
        names=names, 
        values=values, 
        title=title,
        color=names,  # Color based on the 'names' column
        color_discrete_sequence=colors  # Use the custom color palette
    )
    return fig

def violin_plot(df, x, y, title=''):
    fig = px.violin(df, x=x, y=y, box=True, title=title,)
    return fig

def box_plot(df, x, y, color, title=''):
    fig = px.box(df, x=x, y=y, color=color, title=title)
    return fig
df['Survival_Status'] = df['Survived'].map({0: 'No', 1: 'Yes'})

def scatter_plot(df, x, y, color=None, title=''):
    fig = px.scatter(df, x=x, y=y, color=color, title=title)
    return fig

def plot_survival_percentage(df, category_column):
    # Calculate total count by category
    total_por_categoria = df[category_column].value_counts()
    
    # Calculate survival percentages
    porcentajes = df.groupby([category_column, 'Survived']).size().unstack()
    porcentajes = porcentajes.div(total_por_categoria, axis=0) * 100
    
    # Determine appropriate sorting for different category types
    if category_column in ['Pclass', 'Fare']:
        porcentajes = porcentajes.sort_index(ascending=False)
    
    # Create the plot
    colors = sns.color_palette("Blues_d", len(porcentajes.columns))
    
    plt.figure(figsize=(10,6))
    plt.style.use('dark_background')
    plt.rcParams['text.color'] = 'white'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['xtick.color'] = 'white'
    plt.rcParams['ytick.color'] = 'white'

    porcentajes.plot(
        kind='barh', 
        stacked=True, 
        color=colors,
        width=0.6
    )
    
    # Configure title and labels with smaller text
    plt.title(f'Survival Percentage by {category_column}', color='white', fontsize=14)  # Adjusted size
    plt.xlabel('Percentage', color='white', fontsize=12)  # Smaller text
    plt.ylabel(category_column, color='white', fontsize=12)  # Smaller text
    plt.legend(labels=['Not Survive', 'Survived'], title='Survival Status', fontsize=6, title_fontsize=8)  # Smaller legend text

    
    # Add percentage labels
    for i, (index, row) in enumerate(porcentajes.iterrows()):
        cumulative = 0
        for j, value in enumerate(row):
            plt.text(
                cumulative + value / 2, 
                i, 
                f'{value:.1f}%', 
                va='center', 
                ha='center', 
                color='white',
                fontweight='bold'
            )
            cumulative += value
    
    plt.tight_layout()
    return plt.gcf()

def plot_alone_passengers(df_solo):
    # Create a Plotly bar chart for Alone Passengers
    fig = px.bar(
        df_solo.groupby(['Pclass']).size().reset_index(name='Count'), 
        x='Pclass', 
        y='Count', 
        title='Pclass Distribution for Alone Passengers',
        labels={'Pclass': 'Passenger Class', 'Count': 'Number of Alone Passengers'},
        color='Pclass',
        color_discrete_sequence=px.colors.sequential.Blues
    )
    return fig

def plot_family_size_survival(df):
    # Calculate survival percentages by family size
    survival_data = df.groupby('FamilySize')['Survived'].mean() * 100
    
    # Create a Plotly bar chart
    fig = px.bar(
        x=survival_data.index, 
        y=survival_data.values, 
        title='Survival Percentage by Family Size',
        labels={'x': 'Family Size', 'y': 'Survival Percentage'},
        color_discrete_sequence=['#4169E1']  # Royal Blue
    )
    fig.update_layout(
        xaxis_title='Family Size',
        yaxis_title='Survival Percentage (%)'
    )
    return fig

#-----------------------------------------------------------------------------------------------------

# Data Sets for Graphics
datos_pclass = {
    'Class': ['Class 1', 'Class 2', 'Class 3'],
    'Cantidad': [
        sum(1 for _ in df['Pclass'] if _ == 1),
        sum(1 for _ in df['Pclass'] if _ == 2),
        sum(1 for _ in df['Pclass'] if _ == 3)]}
datos_pclass_df = pd.DataFrame(datos_pclass)

df_solo = df[df['Alone'] == 1]

df_filtered = df[df['FamilySize'] != 0]

datos_family = pd.DataFrame({
    'Family Size': ['1', '2', '3', '4', '5', '6', '7', '10'],
    'Cantidad': [
        sum(1 for _ in df['FamilySize'] if _ == 1),
        sum(1 for _ in df['FamilySize'] if _ == 2),
        sum(1 for _ in df['FamilySize'] if _ == 3),
        sum(1 for _ in df['FamilySize'] if _ == 4),
        sum(1 for _ in df['FamilySize'] if _ == 5),
        sum(1 for _ in df['FamilySize'] if _ == 6),
        sum(1 for _ in df['FamilySize'] if _ == 7),
        sum(1 for _ in df['FamilySize'] if _ == 10)
    ]
})

# Calcular los porcentajes
total_por_family = df['FamilySize'].value_counts()
porcentajes = df.groupby(['FamilySize', 'Survived']).size().unstack()
porcentajes = porcentajes.div(total_por_family, axis=0) * 100

# Reordenar los índices según el orden deseado
orden_family = [ 10, 7, 6, 5, 4, 3, 2, 1, 0]  # Orden deseado
porcentajes = porcentajes.reindex(orden_family)

#-----------------------------------------------------------------------------------------------------

# Page: Introduction
def introduction_page():
    st.title('🚢 Introduction to the Titanic')
    
    st.image('streamlitenv/app/Photos/portada_titanic.png', caption='RMS Titanic', width=500)
    
    tab1, tab2 = st.tabs(['🌊 Introduction', '📖 History'])
    
    with tab1: 
        st.markdown("""
    ## Titanic's History
    
    The RMS Titanic was a famous British transatlantic ship that sank on its maiden voyage on April 15, 1912. 
    Considered the largest and most luxurious ship of its time, the Titanic sank after colliding with an iceberg 
    in the Atlantic Ocean, resulting in the loss of more than 1,500 lives.
    
    ### Key Facts:
    - **Construction Period**: 1909-1911
    - **Sinking Date**: April 15, 1912
    - **Location**: North Atlantic Ocean
    - **Passengers**: Approximately 2,224
    - **Casualties**: More than 1,500
    """)
    
    with tab2:
        st.markdown("""
    RMS Titanic was a British ocean liner that sank in the early hours of 15 April 1912 as a result of striking an iceberg on her maiden voyage from Southampton, England, to New York City, United States. It was the second time White Star Line had lost a ship on its maiden voyage, the first being the RMS Tayleur in 1854. Of the estimated 2,224 passengers and crew aboard, approximately 1,500 died, making the incident one of the deadliest peacetime sinkings of a single ship. Titanic, operated by the White Star Line, carried some of the wealthiest people in the world, as well as hundreds of emigrants from the British Isles, Scandinavia, and elsewhere in Europe who were seeking a new life in the United States and Canada. The disaster drew public attention, spurred major changes in maritime safety regulations, and inspired a lasting legacy in popular culture.
        
    RMS Titanic was the largest ship afloat upon entering service and the second of three Olympic-class ocean liners built for the White Star Line. The ship was built by the Harland and Wolff shipbuilding company in Belfast. Thomas Andrews Jr., the chief naval architect of the shipyard, died in the disaster. Titanic was under the command of Captain Edward John Smith, who went down with the ship.
        
    The first-class accommodation was designed to be the pinnacle of comfort and luxury. It included a gymnasium, swimming pool, smoking rooms, fine restaurants and cafes, a Victorian-style Turkish bath, and hundreds of opulent cabins. A high-powered radiotelegraph transmitter was available to send passenger "marconigrams" and for the ship's operational use. Titanic had advanced safety features, such as watertight compartments and remotely activated watertight doors, which contributed to the ship's reputation as "unsinkable".
        
    Titanic was equipped with sixteen lifeboat davits, each capable of lowering three lifeboats, for a total capacity of 48 boats. Despite this capacity, the ship was scantly equipped with a total of only twenty lifeboats. Fourteen of these were regular lifeboats, two were cutter lifeboats, and four were collapsible and proved difficult to launch while the ship was sinking. Together, the lifeboats could hold 1,178 people — roughly half the number of passengers on board, and a third of the number of passengers the ship could have carried at full capacity (a number consistent with the maritime safety regulations of the era). The British Board of Trade's regulations required fourteen lifeboats for a ship of 10,000 tonnes. Titanic carried six more than required, allowing 338 extra people room in lifeboats. When the ship sank, the lifeboats that had been lowered were only filled up to an average of 60%.
    """)


#-----------------------------------------------------------------------------------------------------

# Update data analysis page with icons and improved Family Size section
def data_analysis_page():
    st.title('🚢 Titanic Data Analysis')
    
    tab1, tab2, tab3 = st.tabs(['📊 Data Frame', '📝 Variables', '📈 Graphics'])
    
    with tab1: 
        st.text('Here is the Data Frame used to work in this project:')
        st.dataframe(df)
        
    with tab2: 
        st.markdown("""
        # Here's a breakdown of the Titanic dataset variables:

        1. `Survived`: Survival outcome
           - 0 = Did not survive
           - 1 = Survived

        2. `Pclass`: Ticket class
           - 1 = First Class
           - 2 = Second Class
           - 3 = Third Class

        3. **Personal Information**
        
        `Sex`: Gender (0 = Male / 1 = Female)
        
        `Age`: Passenger's age

        4. **Family Relationships**
        
        `Family Size`: Number of companions aboard
        
        `Alone`: Number of passengers travelling alone

        5. **Travel Details**
        
        `Fare`: Passenger ticket price
        
        `Embarked`: Port of embarkation
           - C = Cheltenham
           - Q = Queenstown
           - S = Southampton
        """)
    
    with tab3: 
        # Visualization Selection
        viz_type = st.selectbox('Select Variable to see the graphics', [
        'Embarked', 
        'Pclass', 
        'Fare',
        'Alone & Family Size'])
        
        if viz_type == 'Embarked':
            st.subheader('Passenger Class Count by Port of Embarkation')
            st.text('People mainly embarked in Southampton, as it was the main port of embarkation.')
            st.text('0 = Southampton 1 = Cheltenham 2 = Queenstown')
            graph1 = count_plot(
            df,
            x='Embarked',
            hue='Pclass',
            title='Pclass by Port of Embarkation')
            st.plotly_chart(graph1)
        
            st.subheader('Percent of Survivors by Port of Embarkation')
            st.text('There are no much differencies on the surival rates depending on the onboarding. Since most of the people embarked on the Southampton port.')
            graph2 = plot_survival_percentage(df, 'Embarked')
            st.pyplot(graph2)
        
        elif viz_type == 'Pclass':
            st.subheader('Passenger Class Distribution')
            st.text("The data visualization highlights that over 50% of passengers on the Titanic traveled in third class, a striking insight that reflects the socio-economic composition of the ship's passengers. A significant reason for this is that many third-class passengers were emigrants seeking a new life in America, drawn to the opportunities promised by the New World.")
            graph3 = pie_chart(
            datos_pclass_df,
            names='Class',
            values='Cantidad',
            title='Pclass Distribution')
            st.plotly_chart(graph3)
            
            st.subheader('Passenger Class Distribution by Age')
            st.text("Passengers from 3rd class are younger compared to the other classes, this could be because are young inmigrants willing to go to New York for the opportunities promised by the New World. The passengers in 1st and 2nd class have a higher mean age, what could be due to have a higher income and could may more than the ones traveling in 3rd class.")
            graph4 = violin_plot(
            df,
            x= 'Pclass',
            y= 'Age',
            title='Pclass Distribution')
            st.plotly_chart(graph4)
            
            st.subheader('Percent of Survivors by Passenger Class')
            st.text('There is a significant difference on the rate on the survival between the 1st and the 2nd class. Traveling on a higher class (1st class) increase the rate of survival.')
            graph5 = plot_survival_percentage(df, 'Pclass')
            st.pyplot(graph5)
        
        elif viz_type == 'Fare':
            st.subheader('Relation of Fare vs Age and Passenger Class')
            st.text("Passengers from 3rd class are younger compared to the other classes, this could be because are young inmigrants willing to go to New York for the opportunities promised by the New World. The passengers in 1st and 2nd class have a higher mean age, what could be due to have a higher income and could may more than the ones traveling in 3rd class.")
            graph6 = scatter_plot(
            df,
            x= 'Age',
            y= 'Fare',
            color= 'Pclass',
            title='Scatter Plot Distribution')
            graph6.update_yaxes(range=[0, 300]) # Y axis limited to 300 for better view
            st.plotly_chart(graph6)
            
            st.subheader('Distribution of Fare by Passenger Class and Survival')
            st.text("Clearly the passengers who paid more, and consequently were in first class have a higher average survival rate. On the other hand, passengers who paid less (both 2nd and 3rd class) do not have such a difference in survivability.")
            graph7 = box_plot(
            df,
            x= 'Pclass',
            y= 'Fare',
            color= 'Survival_Status',
            title='Box Plot Distributionof Fare by Passenger Class and Survival')
            graph7.update_yaxes(range=[0, 300]) # Y axis limited to 300 for better view
            st.plotly_chart(graph7)
        
        elif viz_type == 'Alone & Family Size':
            st.subheader('Alone Passengers Distribution')
            st.text('Most alone people traveled on 3rd class, probably because of emigration.')
            graph8 = plot_alone_passengers(df_solo)
            st.plotly_chart(graph8)
            
            st.subheader('Family Passengers Distribution')
            st.text('Most people traveled with one or two companions, and small groups traveled with big families.')
            graph9 = pie_chart(
            datos_family,
            names='Family Size',
            values='Cantidad',
            title='Family Size Distribution')
            st.plotly_chart(graph9)
            
            st.subheader('Family Passengers Count by Passenger Class')
            st.text('Small families travelled more on 1st class compared to the other ones. While the Family Size grows passengers traveled on 3rd class.')
            graph10 = px.bar(
            df_filtered.groupby(['FamilySize', 'Pclass']).size().reset_index(name='Count'),
            x='FamilySize',
            y='Count',
            color='Pclass',
            title='Family Size count by Pclass',
            labels={'Family Size': 'Family Size', 'Count': 'Number of Passengers'},
            color_discrete_sequence=px.colors.sequential.Blues)
            st.plotly_chart(graph10)
            
            st.subheader('Relation of Fare vs Family Size and Passenger Class')
            st.text("For smaller traveling groups people could afford to pay more and went in 1st class. For bigger families they traveled more on 2nd and 3rd class.")
            graph11 = scatter_plot(
            df,
            x='FamilySize',
            y='Fare',
            color='Pclass',
            title='Scatter Plot Distribution')
            graph11.update_yaxes(range=[0, 300])
            st.plotly_chart(graph11)
            
            st.subheader('Percent of Survivors by Family Size')
            st.text('Survival rates vary depending on family size, with some interesting patterns.')
            graph12 = plot_survival_percentage(df, 'FamilySize')
            st.plotly_chart(graph12)

#-----------------------------------------------------------------------------------------------------

# Page: Conclusions
def conclusions_page():
    st.title('🔎 Analysis Conclusions')
    
    st.markdown("""
    ## General Findings
    
    1. **Gender**: Women had significantly higher survival rates.
    2. **Social Class**: First-class passengers had higher survival rates.
    3. **Age**: Children also had higher chances of survival.
    
    ### Specific Findings
    
    1. **Embarked**: The analysis showed that the port of embarkation did not have a significant impact on the survival rates. Passengers who boarded the Titanic from Cherbourg (C), Queenstown (Q), or Southampton (S) had similar survival probabilities, with no notable differences in the ratios among these groups.
    
    2. **Pclass**: There was a clear correlation between passenger class and survival rate. Passengers in the 1st class had a significantly higher likelihood of survival compared to those in the 2nd and 3rd classes. This could be attributed to better access to lifeboats and other resources for first-class passengers, highlighting a socioeconomic disparity in survival outcomes.
    
    3. **Fare**: The fare paid by passengers appeared to be closely linked to their ticket class (Pclass). As expected, passengers who paid higher fares were generally in the 1st class and therefore experienced better survival rates. This connection underscores the importance of economic factors in determining access to safety during the disaster.
    
    4. **Alone**: Passengers  traveling alone did not show a significant difference in survival rates.
    
    5. **Family Size**: Family size, however, did play a role. Passengers from smaller families (e.g., 2-4 members) had better survival rates compared to those traveling alone or in very large families. Large family groups may have faced challenges in staying together during the chaos, which could have negatively impacted their survival.
    
    The Titanic analysis demonstrates how social and demographic factors 
    can dramatically influence survival possibilities in emergency situations.
    """)

#----------------------------------------------------------------------------------------------

# Page: About Me
def about_me_page():
    st.title('🌷 About Me')
    col1, col2 = st.columns(2)
    with col1: 
        st.image('streamlitenv/app/Photos/Claudia.png', caption='Clàudia Ondategui', width=500)
    with col2: 
        st.markdown("""
    # Hello I'm Clàudia!
    Data analyst on training with Upgrade Hub, doing a 6 months bootcamp.
    
    ## Background
    I have more than 5 years of experience as a Social Media Manager, where I’ve had the opportunity to lead and execute high-impact social media strategies across various industries.
    Throughout my career, I’ve been responsible for creating content, managing campaigns, and building strong relationships with clients. I’ve developed expertise in project coordination, audience engagement, and team leadership, ensuring that every initiative is delivered on time and achieves its objectives.
    
    In addition to my hands-on experience in social media management, I’ve honed my ability to use data-driven insights to refine strategies and optimize campaign performance.
    As my career evolves, I’m now shifting my focus toward deepening my expertise in data analysis.
    """)

#----------------------------------------------------------------------------------------------

# Main App Configuration
def main():
    # Set page configuration
    st.set_page_config(
        page_title='TITANIC ANALYSIS DASHBOARD', 
        page_icon='🚢', 
        layout='wide'
    )
    
    # Apply blue theme
    set_blue_theme()
    
    # Sidebar navigation with icons
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Introduction", "Data Analysis", "Conclusions", "About Me"],
            icons=['house', 'bar-chart', 'list-task', 'person'],
            menu_icon="ship",
            default_index=0,
        )
    
    # Render pages based on sidebar selection
    if selected == "Introduction":
        introduction_page()
    elif selected == "Data Analysis":
        data_analysis_page()
    elif selected == "Conclusions":
        conclusions_page()
    else:
        about_me_page()

if __name__ == '__main__':
    main()