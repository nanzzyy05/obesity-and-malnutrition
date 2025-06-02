import streamlit as st
import pandas as pd
import mysql.connector
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import time

conn = mysql.connector.connect(host = "localhost",user = "root",password = "12345",database = "my_database")
curr = conn.cursor()
conn.commit()

if __name__ == "__main__":
    st.title(":blue[GLOBAL VIEW ON OBESITY AND MALNUTRITION🌏]")

page = st.sidebar.radio("Navigation", ("Queries📝", "EDA visualization📊"))

if page == "Queries📝":
    st.title("OBESITY AND MALNUTRITION")

    query = st.selectbox("choose query",[
    "1.Top 5 regions with the highest average obesity levels in the most recent year(2022)",
    "2.Top 5 countries with highest obesity estimates",
    "3.Obesity trend in India over the years(Mean_estimate)",
    "4.Average obesity by gender",
    "5.Country count by obesity level category and age group",
    "6.Top 5 countries least reliable countries(with highest CI_Width) and Top 5 most consistent countries (smallest average CI_Width",
    "7.Average obesity by age group",
    "8.Top 10 Countries with consistent low obesity (low average + low CI)over the years",
    "9.Countries where female obesity exceeds male by large margin (same year)",
    "10.Global average obesity percentage per year",
    "11.Avg. malnutrition by age group",
    "12.Top 5 countries with highest malnutrition(mean_estimate)",
    "13.Malnutrition trend in African region over the years",
    "14.Gender-based average malnutrition",
    "15.Malnutrition level-wise (average CI_Width by age group)",
    "16.Yearly malnutrition change in specific countries(India, Nigeria, Brazil)",
    "17.Regions with lowest malnutrition averages",
    "18.Countries with increasing malnutrition (💡 Hint: Use MIN() and MAX()   on Mean_Estimate per country to compare early vs. recent malnutrition levels, and filter where the difference is positive using HAVING.)",
    "19.Min/Max malnutrition levels year-wise comparison",
    "20.High CI_Width flags for monitoring(CI_width > 5)",
    "21.Obesity vs malnutrition comparison by country(any 5 countries)",
    "22.Gender-based disparity in both obesity and malnutrition",
    "23.Region-wise avg estimates side-by-side(Africa and America)",
    "24.Countries with obesity up & malnutrition down",
    "25.Age-wise trend analysis"

    ])    

    with st.spinner("Wait for it..."):
        time.sleep(2)
    st.success("Done!")

    if query == "1.Top 5 regions with the highest average obesity levels in the most recent year(2022)":
        curr.execute("""
        SELECT
        region,
        AVG(obesity_level) AS average_obesity
    FROM
        obesity
    WHERE
        year = 2022
    GROUP BY
        region
    ORDER BY
        average_obesity DESC
    LIMIT 5;
        """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Region', 'Average Obesity'])
        st.dataframe(df)

    elif query == "2.Top 5 countries with highest obesity estimates":
        curr.execute("""
        SELECT
        country,
        mean_estimate AS highest_obesity
    FROM
        obesity
    ORDER BY
        mean_estimate DESC
    LIMIT 5;
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Country', 'Highest Obesity'])
        st.dataframe(df)
        
    elif query == "3.Obesity trend in India over the years(Mean_estimate)":
        curr.execute("""
        SELECT
        year,
        mean_estimate AS obesity_trend
    FROM
        obesity
    WHERE
        country = 'India'
    ORDER BY
        year;
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Year', 'Obesity Trend'])
        st.dataframe(df)

    elif query == "4.Average obesity by gender":
        curr.execute("""
        SELECT
        gender,
        AVG(mean_estimate) AS average_obesity
    FROM
        obesity
    GROUP BY
        gender;
    """)        
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['gender', 'Average Obesity'])
        st.dataframe(df)

    elif query == "5.Country count by obesity level category and age group":
        curr.execute("""
        SELECT
        age_group,
        obesity_level,
        COUNT(country) AS country_count
    FROM
        obesity
    GROUP BY
        age_group, obesity_level
    ORDER BY
        age_group, obesity_level;
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Age Group', 'Obesity Level', 'Country Count'])
        st.dataframe(df)

    elif query == "6.Top 5 countries least reliable countries(with highest CI_Width) and Top 5 most consistent countries (smallest average CI_Width":
        curr.execute("""
        SELECT
        country,
        AVG(ci_width) AS average_ci_width
    FROM
        obesity
    GROUP BY
        country
    ORDER BY
        average_ci_width DESC
    LIMIT 5;
    """)
        results = curr.fetchall()
        df_least_reliable = pd.DataFrame(results, columns=['Country', 'Average CI Width'])
        st.dataframe(df_least_reliable)

    elif query == "7.Average obesity by age group":
        curr.execute("""
        SELECT
        age_group,
        AVG(mean_estimate) AS average_obesity
    FROM
        obesity
    GROUP BY
        age_group
    ORDER BY
        age_group;
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Age Group', 'Average Obesity'])
        st.dataframe(df)

    elif query == "8.Top 10 Countries with consistent low obesity (low average + low CI)over the years":
        curr.execute("""
        SELECT
        country,
        AVG(mean_estimate) AS average_obesity,
        AVG(ci_width) AS average_ci_width
    FROM
        obesity
    GROUP BY
        country
    HAVING
        average_obesity < 10 AND average_ci_width < 2
    ORDER BY
        average_obesity, average_ci_width
    LIMIT 10;
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Country', 'Average Obesity', 'Average CI Width'])
        st.dataframe(df)

    elif query == "9.Countries where female obesity exceeds male by large margin (same year)":
        curr.execute("""
        SELECT
        f.country,
        f.year,
        f.average_female_obesity,
        m.average_male_obesity
    FROM
        (SELECT country, year, AVG(mean_estimate) AS average_female_obesity
        FROM obesity
        WHERE gender = 'Female'
        GROUP BY country, year) AS f
    JOIN
        (SELECT country, year, AVG(mean_estimate) AS average_male_obesity
        FROM obesity
        WHERE gender = 'Male'
        GROUP BY country, year) AS m
    ON
        f.country = m.country AND f.year = m.year
    ORDER BY
        f.country, f.year;
        """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Country', 'Year', 'Average Female Obesity', 'Average Male Obesity'])
        st.dataframe(df)

    elif query == "10.Global average obesity percentage per year":
        curr.execute("""
        SELECT
        year,
        AVG(mean_estimate) AS global_average_obesity
    FROM
        obesity
    GROUP BY
        year
    ORDER BY
        year;
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Year', 'Global Average Obesity'])
        st.dataframe(df)

    elif query == "11.Avg. malnutrition by age group":
        curr.execute("""
        SELECT
        age_group,
        AVG(mean_estimate) AS average_malnutrition
    FROM
        malnutrition
    GROUP BY
        age_group
    ORDER BY
        age_group;
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Age Group', 'Average Malnutrition'])
        st.dataframe(df)

    elif query == "12.Top 5 countries with highest malnutrition(mean_estimate)":
        curr.execute("""
        SELECT
        country,
        mean_estimate AS highest_malnutrition
    FROM
        malnutrition
    ORDER BY
        mean_estimate DESC
    LIMIT 5;
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Country', 'Highest Malnutrition'])
        st.dataframe(df)

    elif query == "13.Malnutrition trend in African region over the years":
        curr.execute("""
        SELECT
        year,
        mean_estimate AS malnutrition_trend
    FROM
        malnutrition
    WHERE
        region = 'Africa'
    ORDER BY
        year;
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Year', 'Malnutrition Trend'])
        st.dataframe(df)

    elif query == "14.Gender-based average malnutrition":
        curr.execute("""
        SELECT
        gender,
        AVG(mean_estimate) AS average_malnutrition
    FROM
        malnutrition
    GROUP BY
        gender;
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['gender', 'Average Malnutrition'])
        st.dataframe(df)
                    

    elif query == "15.Malnutrition level-wise (average CI_Width by age group)":
        curr.execute("""
        SELECT
        malnutrition_level,
        age_group,
        AVG(CI_Width) AS average_ci_width
    FROM
        malnutrition
    GROUP BY
        malnutrition_level,
        age_group
    ORDER BY
        malnutrition_level,
        age_group;   
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Age Group', 'Average CI Width', 'Malnutrition Level'])
        st.dataframe(df)
                    

    elif query == "16.Yearly malnutrition change in specific countries(India, Nigeria, Brazil)":
        curr.execute("""
        SELECT
        year,
        country,
        mean_estimate AS malnutrition_change
    FROM
        malnutrition
    WHERE
        country IN ('India', 'Nigeria', 'Brazil')
    ORDER BY
        country, year;
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Year', 'Country', 'Malnutrition Change'])
        st.dataframe(df)


    elif query == "17.Regions with lowest malnutrition averages":
        curr.execute("""
        SELECT
        region,
        AVG(mean_estimate) AS average_malnutrition
    FROM
        malnutrition
    GROUP BY
        region
    ORDER BY
        average_malnutrition ASC
    LIMIT 5;
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Region', 'Average Malnutrition'])
        st.dataframe(df)

    elif query == "18.Countries with increasing malnutrition (💡 Hint: Use MIN() and MAX()   on Mean_Estimate per country to compare early vs. recent malnutrition levels, and filter where the difference is positive using HAVING.)":
        curr.execute("""
        SELECT
        country,
        MIN(mean_estimate) AS min_malnutrition,
        MAX(mean_estimate) AS max_malnutrition
    FROM
        malnutrition
    GROUP BY
        country
    HAVING
        MAX(mean_estimate) > MIN(mean_estimate)
    ORDER BY
        country;
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Country', 'Min Malnutrition', 'Max Malnutrition'])
        st.dataframe(df)


    elif query == "19.Min/Max malnutrition levels year-wise comparison":
        curr.execute("""
        SELECT
        year,
        MIN(mean_estimate) AS min_malnutrition,
        MAX(mean_estimate) AS max_malnutrition
    FROM
        malnutrition
    GROUP BY
        year
    ORDER BY
        year;
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Year', 'Min Malnutrition', 'Max Malnutrition'])
        st.dataframe(df)


    elif query == "20.High CI_Width flags for monitoring(CI_width > 5)":
        curr.execute("""
        SELECT
        country,
        year,
        ci_width
    FROM
        malnutrition
    WHERE
        ci_width > 5
    ORDER BY
        country, year;
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Country', 'Year', 'CI Width'])
        st.dataframe(df)


    elif query == "21.Obesity vs malnutrition comparison by country(any 5 countries)":
        curr.execute("""
        SELECT
        o.country,
        AVG(o.mean_estimate) AS average_obesity,
        AVG(m.mean_estimate) AS average_malnutrition
    FROM
        obesity AS o
    JOIN
        malnutrition AS m ON o.country = m.country
    GROUP BY
        o.country
    ORDER BY
        o.country
    LIMIT 5;
        
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Country','Obesity Estimate', 'Malnutrition Estimate'])
        st.dataframe(df)


    elif query == "22.Gender-based disparity in both obesity and malnutrition":
        curr.execute("""
        SELECT
        o.gender,
        o.average_obesity,
        m.average_malnutrition
    FROM
        (SELECT gender, AVG(Mean_Estimate) AS average_obesity FROM obesity GROUP BY gender) AS o
    LEFT JOIN
        (SELECT gender, AVG(mean_estimate) AS average_malnutrition FROM malnutrition GROUP BY gender) AS m
    ON
        o.gender = m.gender; 
                """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['gender', 'Average Obesity', 'Average Malnutrition'])
        st.dataframe(df)  


    elif query == "23.Region-wise avg estimates side-by-side(Africa and America)":
        curr.execute("""
        SELECT
        region,
        AVG(mean_estimate) AS average_obesity,
        AVG(mean_estimate) AS average_malnutrition
    FROM
        (SELECT region, mean_estimate FROM obesity WHERE region IN ('Africa', 'Americas')
        UNION ALL
        SELECT region, mean_estimate FROM malnutrition WHERE region IN ('Africa', 'Americas')) AS combined
    GROUP BY
        region
    ORDER BY
        region;
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Region', 'Average Obesity', 'Average Malnutrition'])
        st.dataframe(df)   


    elif query == "24.Countries with obesity up & malnutrition down":
        curr.execute("""
        SELECT
        o.country,
        o.mean_estimate,
        m.mean_estimate
    FROM
        obesity AS o
    JOIN
        malnutrition AS m ON o.country = m.country AND o.year = m.year
    WHERE
        o.year = 2022 
        AND o.mean_estimate >= 30 
        AND m.mean_estimate < 10
        limit 100; 
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Country', 'Average Obesity', 'Average Malnutrition'])
        st.dataframe(df)


    elif query == "25.Age-wise trend analysis":
        curr.execute("""
        SELECT
        age_group,
        AVG(mean_estimate) AS average_obesity,
        AVG(mean_estimate) AS average_malnutrition
    FROM
        (SELECT age_group, year, mean_estimate FROM obesity
        UNION ALL
        SELECT age_group, year, mean_estimate FROM malnutrition) AS combined
    GROUP BY
        age_group
    ORDER BY
        age_group;
    """)
        results = curr.fetchall()
        df = pd.DataFrame(results, columns=['Age Group','Average Obesity', 'Average Malnutrition'])
        st.dataframe(df)


if page == "EDA visualization📊":
    st.title("EDA Visualization📊")

    # Load obesity data
    curr.execute("SELECT age_group, Mean_Estimate FROM obesity")
    obesity = pd.DataFrame(curr.fetchall(), columns=['age_group', 'Mean_Estimate'])

    # Load malnutrition data
    curr.execute("SELECT age_group, Mean_Estimate FROM malnutrition")
    malnutrition = pd.DataFrame(curr.fetchall(), columns=['age_group', 'Mean_Estimate'])

    # comparing obesity and malnutrition trends
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=obesity, x='age_group', y='Mean_Estimate', label='Obesity', color='red')
    sns.lineplot(data=malnutrition, x='age_group', y='Mean_Estimate', label='Malnutrition', color='blue')
    plt.title('Obesity vs Malnutrition Trends (2012-2022)')
    plt.xlabel('age_group')
    plt.ylabel('Mean BMI')
    plt.legend()
    st.pyplot(plt.gcf())


# Finding which region has the highest obesity and malnutrition rate

    curr.execute("""
    SELECT region, 
           AVG(CASE WHEN source = 'obesity' THEN Mean_Estimate END) AS Avg_Obesity,
           AVG(CASE WHEN source = 'malnutrition' THEN Mean_Estimate END) AS Avg_Malnutrition
    FROM (
        SELECT region, Mean_Estimate, 'obesity' AS source FROM obesity
        UNION ALL
        SELECT region, Mean_Estimate, 'malnutrition' AS source FROM malnutrition
    ) AS combined
    GROUP BY region
""")
    df = pd.DataFrame(curr.fetchall(), columns=['Region', 'Avg_Obesity', 'Avg_Malnutrition'])

# Melt the dataframe for plotting
    df_melted = df.melt(id_vars='Region', value_vars=['Avg_Obesity', 'Avg_Malnutrition'],
                    var_name='Type', value_name='Average')

# Pie chart: show both obesity and malnutrition by region (as a sunburst for clarity)
    fig = px.pie(
    df_melted,
    names='Region',
    values='Average',
    hole=0.5,
    title="Obesity and Malnutrition Rate by Region (Donut Chart)",
    width=600,
    height=500,
    )
    st.plotly_chart(fig)


# Histogram comparison of obesity and malnutrition levels
    curr.execute("SELECT obesity_level FROM obesity")
    df_obesity = pd.DataFrame(curr.fetchall(), columns=['obesity_level'])

    curr.execute("SELECT malnutrition_level FROM malnutrition")
    df_malnutrition = pd.DataFrame(curr.fetchall(), columns=['malnutrition_level'])

    fig, axes = plt.subplots(1, 2, figsize=(15, 8))
    sns.histplot(data=df_obesity, x='obesity_level', color='red', ax=axes[0])
    axes[0].set_title('Obesity Level Distribution')
    sns.histplot(data=df_malnutrition, x='malnutrition_level', color='blue', ax=axes[1])
    axes[1].set_title('Malnutrition Level Distribution')
    plt.suptitle('Obesity and Malnutrition Levels')
    st.pyplot(fig)

# line plot for the first 20 records of obesity and malnutrition trends
    plt.figure(figsize=(25, 12))
    sns.set_style("whitegrid")
    data_obesity = obesity.head(20).reset_index(drop=True)
    data_malnutrition = malnutrition.head(20).reset_index(drop=True)
    sns.lineplot(data=data_obesity, x=data_obesity.index, y="Mean_Estimate", marker='o', color='green', label="Obesity")
    sns.lineplot(data=data_malnutrition, x=data_malnutrition.index, y="Mean_Estimate", marker='o', color='orange', label="Malnutrition")
    plt.title('Obesity and Malnutrition Trends for the First 20 Records')
    plt.xlabel('Record Index')
    plt.ylabel('Mean Estimate')
    plt.legend()
    st.pyplot(plt.gcf())


# Fetch CI_Width data for obesity
    curr.execute("SELECT CI_Width FROM obesity")
    df_ci_width = pd.DataFrame(curr.fetchall(), columns=['CI_Width'])

    plt.figure(figsize=(20, 14))
    sns.histplot(data=df_ci_width, x="CI_Width", color='black')
    plt.xlabel('CI Width')
    plt.title('CI Width for Obesity Data')
    plt.ylabel('Count')
    st.pyplot(plt.gcf())


# Gender-wise barplot for Obesity
    curr.execute("SELECT gender AS Gender, AVG(Mean_Estimate) AS Mean_Estimate FROM obesity GROUP BY gender")
    df_obesity = pd.DataFrame(curr.fetchall(), columns=["Gender", "Mean_Estimate"])

    plt.figure(figsize=(8, 5))
    ax = sns.barplot(data=df_obesity, x="Gender", y="Mean_Estimate", color="pink", errorbar=None)
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', padding=5)
    plt.title("Obesity Across Genders")
    plt.xlabel("Gender")
    plt.ylabel("Mean Estimate")
    st.pyplot(plt.gcf())

# Gender-wise barplot for Malnutrition
    curr.execute("SELECT gender AS Gender, AVG(Mean_Estimate) AS Mean_Estimate FROM malnutrition GROUP BY gender")
    df_malnutrition = pd.DataFrame(curr.fetchall(), columns=["Gender", "Mean_Estimate"])

    plt.figure(figsize=(8, 5))
    ax = sns.barplot(data=df_malnutrition, x="Gender", y="Mean_Estimate", color="purple", errorbar=None)
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', padding=5)
    plt.title("Malnutrition Across Genders")
    plt.xlabel("Gender")
    plt.ylabel("Mean Estimate")
    st.pyplot(plt.gcf())

# Feedback section
    st.subheader("Feedback Section👍🏽")
    sentiment_mapping = ["one", "two", "three", "four", "five"]
    selected = st.feedback("stars")
    if selected is not None:
        st.markdown(f"Thank you for selecting {sentiment_mapping[selected]} star(s).")
