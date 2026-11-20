"""
CareerCompass - Career Data, Domain Definitions, 100 MCQ Question Bank, and Roadmaps.

This module provides:
1. CAREER_DOMAINS: The 5 core domains, required skills, and 3-stage curated learning roadmaps.
2. ALL_TECHNICAL_SKILLS & ALL_INTERESTS: Standard taxonomy for student profiles.
3. QUESTIONS: 100 original, technically sound MCQs (20 per domain, 12 basic + 8 practical).
4. Helper functions to sample 25 questions (3 basic + 2 practical per domain) and evaluate recommendations.
"""

import random

CAREER_DOMAINS = {
    "data_analytics": {
        "id": "data_analytics",
        "title": "Data Analytics",
        "description": "Transform raw business data into actionable visual insights, interactive dashboards, and strategic metrics.",
        "core_skills": ["Python", "SQL", "Statistics", "Power BI"],
        "potential_roles": ["Data Analyst", "Business Intelligence (BI) Developer", "Reporting Analyst", "Operations Analyst"],
        "roadmap": {
            "stage_1": {
                "name": "Stage 1 – Beginner",
                "summary": "Build strong foundations in data manipulation, SQL queries, and core descriptive statistics.",
                "tasks": [
                    {
                        "id": "da_s1_t1",
                        "title": "Learn Relational Databases & SQL Querying",
                        "description": "Understand tables, SELECT, WHERE filtering, aggregate functions, GROUP BY, and JOIN operations.",
                        "skills": ["SQL"],
                        "resources": [
                            {"name": "SQLBolt – Interactive SQL Lessons", "url": "https://sqlbolt.com/"},
                            {"name": "W3Schools – SQL Tutorial", "url": "https://www.w3schools.com/sql/"}
                        ]
                    },
                    {
                        "id": "da_s1_t2",
                        "title": "Python for Data Analysis Fundamentals",
                        "description": "Master Python syntax, lists, dictionaries, pandas DataFrames, and NumPy array basics.",
                        "skills": ["Python"],
                        "resources": [
                            {"name": "Python Official Tutorial", "url": "https://docs.python.org/3/tutorial/"},
                            {"name": "freeCodeCamp – Data Analysis with Python", "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/"}
                        ]
                    },
                    {
                        "id": "da_s1_t3",
                        "title": "Foundational Descriptive Statistics",
                        "description": "Study mean, median, mode, standard deviation, interquartile ranges, and standard distributions.",
                        "skills": ["Statistics"],
                        "resources": [
                            {"name": "Kaggle Learn – Intro to Statistics", "url": "https://www.kaggle.com/learn"},
                            {"name": "Khan Academy – Statistics and Probability", "url": "https://www.khanacademy.org/math/statistics-probability"}
                        ]
                    }
                ]
            },
            "stage_2": {
                "name": "Stage 2 – Intermediate",
                "summary": "Advance to business intelligence tools, window functions, and interactive dashboard storytelling.",
                "tasks": [
                    {
                        "id": "da_s2_t1",
                        "title": "Power BI Modeling & DAX Expressions",
                        "description": "Learn Power Query ETL, star-schema data modeling, calculated columns, and core DAX measures.",
                        "skills": ["Power BI"],
                        "resources": [
                            {"name": "Microsoft Learn – Get Started with Power BI", "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi"},
                            {"name": "freeCodeCamp – Power BI for Beginners", "url": "https://www.freecodecamp.org/news/learn-power-bi/"}
                        ]
                    },
                    {
                        "id": "da_s2_t2",
                        "title": "Advanced SQL & Analytical Windows",
                        "description": "Master SQL window functions (ROW_NUMBER, RANK, LAG, LEAD), CTEs, and query optimization.",
                        "skills": ["SQL"],
                        "resources": [
                            {"name": "Mode Analytics SQL Tutorial", "url": "https://mode.com/sql-tutorial/"},
                            {"name": "Kaggle Learn – Advanced SQL", "url": "https://www.kaggle.com/learn/advanced-sql"}
                        ]
                    },
                    {
                        "id": "da_s2_t3",
                        "title": "Data Visualization with Python",
                        "description": "Create publication-quality charts using Matplotlib and Seaborn to tell visual stories.",
                        "skills": ["Python", "Statistics"],
                        "resources": [
                            {"name": "Kaggle Learn – Data Visualization", "url": "https://www.kaggle.com/learn/data-visualization"}
                        ]
                    }
                ]
            },
            "stage_3": {
                "name": "Stage 3 – Practical Projects",
                "summary": "Produce portfolio-grade analytics case studies with end-to-end business insights.",
                "tasks": [
                    {
                        "id": "da_s3_t1",
                        "title": "E-Commerce Customer & Sales Performance Dashboard",
                        "description": "Ingest multi-table sales data, model relationships in Power BI, and build an executive KPI dashboard.",
                        "skills": ["Power BI", "SQL", "Statistics"],
                        "resources": [
                            {"name": "Kaggle Public Datasets", "url": "https://www.kaggle.com/datasets"}
                        ]
                    },
                    {
                        "id": "da_s3_t2",
                        "title": "Exploratory Cohort & Churn Analysis in Python",
                        "description": "Clean customer subscription logs with pandas, compute monthly retention cohorts, and visualize trends.",
                        "skills": ["Python", "Statistics"],
                        "resources": [
                            {"name": "pandas Documentation & Case Studies", "url": "https://pandas.pydata.org/docs/"}
                        ]
                    }
                ]
            }
        }
    },

    "machine_learning_ai": {
        "id": "machine_learning_ai",
        "title": "Machine Learning / Artificial Intelligence",
        "description": "Design and train algorithmic systems that learn patterns from data to make automated predictions and decisions.",
        "core_skills": ["Python", "Machine Learning Algorithms", "Mathematics"],
        "potential_roles": ["Machine Learning Engineer", "AI Researcher", "Algorithm Developer", "Predictive Modeler"],
        "roadmap": {
            "stage_1": {
                "name": "Stage 1 – Beginner",
                "summary": "Master core Python scientific computing, linear algebra, multivariable calculus, and supervised basics.",
                "tasks": [
                    {
                        "id": "ml_s1_t1",
                        "title": "Mathematics for Machine Learning Essentials",
                        "description": "Solidify vectors, matrix transformations, eigenvalues, partial derivatives, and gradient descent intuition.",
                        "skills": ["Mathematics"],
                        "resources": [
                            {"name": "Khan Academy – Linear Algebra", "url": "https://www.khanacademy.org/math/linear-algebra"},
                            {"name": "Khan Academy – Multivariable Calculus", "url": "https://www.khanacademy.org/math/multivariable-calculus"}
                        ]
                    },
                    {
                        "id": "ml_s1_t2",
                        "title": "Python Scientific Stack (NumPy & SciPy)",
                        "description": "Master array broadcasting, vectorized linear algebra operations, and mathematical computations.",
                        "skills": ["Python", "Mathematics"],
                        "resources": [
                            {"name": "NumPy Official Quickstart", "url": "https://numpy.org/doc/stable/user/quickstart.html"}
                        ]
                    },
                    {
                        "id": "ml_s1_t3",
                        "title": "Introductory Supervised Learning with scikit-learn",
                        "description": "Understand linear regression, logistic regression, decision trees, and train/test splits.",
                        "skills": ["Machine Learning Algorithms"],
                        "resources": [
                            {"name": "Kaggle Learn – Intro to Machine Learning", "url": "https://www.kaggle.com/learn/intro-to-machine-learning"},
                            {"name": "Google Machine Learning Crash Course", "url": "https://developers.google.com/machine-learning/crash-course"}
                        ]
                    }
                ]
            },
            "stage_2": {
                "name": "Stage 2 – Intermediate",
                "summary": "Deepen expertise in ensemble algorithms, hyperparameter tuning, and cross-validation.",
                "tasks": [
                    {
                        "id": "ml_s2_t1",
                        "title": "Ensemble Methods & Tree-Based Models",
                        "description": "Implement Random Forests, AdaBoost, Gradient Boosting, and XGBoost with hyperparameter search.",
                        "skills": ["Machine Learning Algorithms", "Python"],
                        "resources": [
                            {"name": "scikit-learn User Guide", "url": "https://scikit-learn.org/stable/user_guide.html"},
                            {"name": "Kaggle Learn – Intermediate Machine Learning", "url": "https://www.kaggle.com/learn/intermediate-machine-learning"}
                        ]
                    },
                    {
                        "id": "ml_s2_t2",
                        "title": "Model Evaluation & Feature Engineering",
                        "description": "Study ROC-AUC, precision-recall curves, confusion matrices, and automated cross-validation.",
                        "skills": ["Machine Learning Algorithms", "Mathematics"],
                        "resources": [
                            {"name": "Google ML Crash Course – Classification Metrics", "url": "https://developers.google.com/machine-learning/crash-course/classification"}
                        ]
                    },
                    {
                        "id": "ml_s2_t3",
                        "title": "Unsupervised Learning & Dimensionality Reduction",
                        "description": "Implement K-Means clustering, hierarchical clustering, and Principal Component Analysis (PCA).",
                        "skills": ["Machine Learning Algorithms", "Mathematics"],
                        "resources": [
                            {"name": "scikit-learn Clustering Guide", "url": "https://scikit-learn.org/stable/modules/clustering.html"}
                        ]
                    }
                ]
            },
            "stage_3": {
                "name": "Stage 3 – Practical Projects",
                "summary": "Deploy production-ready machine learning pipelines with complete validation.",
                "tasks": [
                    {
                        "id": "ml_s3_t1",
                        "title": "End-to-End Loan Default / Fraud Prediction Model",
                        "description": "Tackle imbalanced tabular data with SMOTE, tune an XGBoost model, and evaluate with precision-recall curves.",
                        "skills": ["Machine Learning Algorithms", "Python"],
                        "resources": [
                            {"name": "Kaggle Competitions Archive", "url": "https://www.kaggle.com/competitions"}
                        ]
                    },
                    {
                        "id": "ml_s3_t2",
                        "title": "Machine Learning Microservice with Flask",
                        "description": "Serialize a trained model with joblib and build a secure REST endpoint for real-time predictions.",
                        "skills": ["Python", "Machine Learning Algorithms"],
                        "resources": [
                            {"name": "Flask Official Documentation", "url": "https://flask.palletsprojects.com/"}
                        ]
                    }
                ]
            }
        }
    },

    "data_science": {
        "id": "data_science",
        "title": "Data Science",
        "description": "Unify scientific experimentation, statistical rigor, data engineering, and machine learning to solve ambiguous problems.",
        "core_skills": ["Python", "SQL", "Statistics", "Machine Learning"],
        "potential_roles": ["Data Scientist", "Decision Scientist", "Quantitative Analyst", "Research Scientist"],
        "roadmap": {
            "stage_1": {
                "name": "Stage 1 – Beginner",
                "summary": "Establish strong foundations across data wrangling, SQL joins, and statistical hypothesis testing.",
                "tasks": [
                    {
                        "id": "ds_s1_t1",
                        "title": "Python Data Wrangling & Cleaning",
                        "description": "Use pandas to clean messy data, handle null values, normalize formats, and parse datetime series.",
                        "skills": ["Python"],
                        "resources": [
                            {"name": "Kaggle Learn – Pandas", "url": "https://www.kaggle.com/learn/pandas"},
                            {"name": "freeCodeCamp Python Curriculum", "url": "https://www.freecodecamp.org/learn"}
                        ]
                    },
                    {
                        "id": "ds_s1_t2",
                        "title": "SQL Querying for Data Extraction",
                        "description": "Extract structured data from multiple tables using subqueries, aggregation, and complex joins.",
                        "skills": ["SQL"],
                        "resources": [
                            {"name": "SQLBolt", "url": "https://sqlbolt.com/"},
                            {"name": "W3Schools SQL", "url": "https://www.w3schools.com/sql/"}
                        ]
                    },
                    {
                        "id": "ds_s1_t3",
                        "title": "Inferential Statistics & Hypothesis Testing",
                        "description": "Master probability distributions, Central Limit Theorem, z-tests, t-tests, and p-value significance.",
                        "skills": ["Statistics"],
                        "resources": [
                            {"name": "Khan Academy – Hypothesis Testing", "url": "https://www.khanacademy.org/math/statistics-probability/significance-tests-one-sample"}
                        ]
                    }
                ]
            },
            "stage_2": {
                "name": "Stage 2 – Intermediate",
                "summary": "Develop end-to-end predictive pipelines and conduct rigorous statistical A/B experiments.",
                "tasks": [
                    {
                        "id": "ds_s2_t1",
                        "title": "Statistical A/B Testing & Experimentation",
                        "description": "Design controlled experiments, calculate minimum sample size, and analyze conversion lift.",
                        "skills": ["Statistics", "Python"],
                        "resources": [
                            {"name": "Google Experimentation Best Practices", "url": "https://developers.google.com/machine-learning"}
                        ]
                    },
                    {
                        "id": "ds_s2_t2",
                        "title": "Predictive Modeling with scikit-learn",
                        "description": "Build classification and regression pipelines with automated preprocessing and column transformers.",
                        "skills": ["Machine Learning", "Python"],
                        "resources": [
                            {"name": "scikit-learn Pipeline Tutorial", "url": "https://scikit-learn.org/stable/modules/compose.html"}
                        ]
                    },
                    {
                        "id": "ds_s2_t3",
                        "title": "Exploratory Data Analysis (EDA) Frameworks",
                        "description": "Execute structured EDA: outlier detection, correlation heatmaps, distribution skewness checks.",
                        "skills": ["Python", "Statistics"],
                        "resources": [
                            {"name": "Kaggle Learn – Data Cleaning", "url": "https://www.kaggle.com/learn/data-cleaning"}
                        ]
                    }
                ]
            },
            "stage_3": {
                "name": "Stage 3 – Practical Projects",
                "summary": "Build end-to-end data products combining statistical experiments and predictive modeling.",
                "tasks": [
                    {
                        "id": "ds_s3_t1",
                        "title": "Healthcare / Patient Risk Prediction Study",
                        "description": "Formulate hypotheses, clean clinical records, train an interpretable model, and present findings.",
                        "skills": ["Python", "Statistics", "Machine Learning"],
                        "resources": [
                            {"name": "UCI Machine Learning Repository", "url": "https://archive.ics.uci.edu/"}
                        ]
                    },
                    {
                        "id": "ds_s3_t2",
                        "title": "Customer Lifetime Value (LTV) & Segmentation Engine",
                        "description": "Combine RFM analysis with K-Means clustering and predictive regression to guide retention marketing.",
                        "skills": ["Python", "SQL", "Statistics", "Machine Learning"],
                        "resources": [
                            {"name": "Kaggle Notebooks Community", "url": "https://www.kaggle.com/code"}
                        ]
                    }
                ]
            }
        }
    },

    "deep_learning_genai": {
        "id": "deep_learning_genai",
        "title": "Deep Learning / Generative AI",
        "description": "Architect deep neural representations, transformer models, prompt engineering pipelines, and LLM applications.",
        "core_skills": ["Neural Networks", "NLP", "Large Language Models (LLMs)"],
        "potential_roles": ["Generative AI Engineer", "NLP Specialist", "Deep Learning Engineer", "Prompt & LLM Solutions Architect"],
        "roadmap": {
            "stage_1": {
                "name": "Stage 1 – Beginner",
                "summary": "Learn artificial neuron mechanics, activation functions, backpropagation, and tokenization basics.",
                "tasks": [
                    {
                        "id": "dl_s1_t1",
                        "title": "Foundations of Artificial Neural Networks",
                        "description": "Understand perceptrons, dense layers, activation functions (ReLU, Sigmoid, Softmax), and backpropagation.",
                        "skills": ["Neural Networks"],
                        "resources": [
                            {"name": "Google Machine Learning – Neural Networks", "url": "https://developers.google.com/machine-learning/crash-course/introduction-to-neural-networks"},
                            {"name": "freeCodeCamp – Deep Learning Fundamentals", "url": "https://www.freecodecamp.org/news"}
                        ]
                    },
                    {
                        "id": "dl_s1_t2",
                        "title": "Introduction to NLP & Text Processing",
                        "description": "Study regular expressions, tokenization, stop-word removal, TF-IDF, and word embeddings.",
                        "skills": ["NLP"],
                        "resources": [
                            {"name": "Kaggle Learn – Natural Language Processing", "url": "https://www.kaggle.com/learn/natural-language-processing"}
                        ]
                    },
                    {
                        "id": "dl_s1_t3",
                        "title": "Deep Learning Frameworks (PyTorch / TensorFlow)",
                        "description": "Build and train your first multi-layer neural network on tabular or image data using PyTorch.",
                        "skills": ["Neural Networks"],
                        "resources": [
                            {"name": "PyTorch Official Tutorials", "url": "https://pytorch.org/tutorials/"}
                        ]
                    }
                ]
            },
            "stage_2": {
                "name": "Stage 2 – Intermediate",
                "summary": "Master Transformer self-attention, pre-trained language models, and prompt engineering strategies.",
                "tasks": [
                    {
                        "id": "dl_s2_t1",
                        "title": "The Transformer Architecture & Self-Attention",
                        "description": "Study multi-head self-attention, encoder-decoder models, positional encodings, and BERT/GPT architectures.",
                        "skills": ["Neural Networks", "NLP"],
                        "resources": [
                            {"name": "Hugging Face – NLP Course", "url": "https://huggingface.co/learn/nlp-course/chapter1/1"}
                        ]
                    },
                    {
                        "id": "dl_s2_t2",
                        "title": "Prompt Engineering & LLM APIs",
                        "description": "Master zero-shot, few-shot, chain-of-thought prompting, temperature tuning, and structured JSON outputs.",
                        "skills": ["Large Language Models (LLMs)"],
                        "resources": [
                            {"name": "OpenAI / Anthropic Prompt Engineering Guides", "url": "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview"}
                        ]
                    },
                    {
                        "id": "dl_s2_t3",
                        "title": "Vector Databases & Semantic Search",
                        "description": "Generate dense vector embeddings and index them with cosine distance for semantic similarity queries.",
                        "skills": ["NLP", "Large Language Models (LLMs)"],
                        "resources": [
                            {"name": "Hugging Face Vector Embeddings Guide", "url": "https://huggingface.co/blog/getting-started-with-embeddings"}
                        ]
                    }
                ]
            },
            "stage_3": {
                "name": "Stage 3 – Practical Projects",
                "summary": "Build practical Generative AI applications using RAG and parameter-efficient fine-tuning.",
                "tasks": [
                    {
                        "id": "dl_s3_t1",
                        "title": "Retrieval-Augmented Generation (RAG) Document Assistant",
                        "description": "Build an AI agent that chunks PDF documents, embeds them, and accurately answers user questions with citations.",
                        "skills": ["Large Language Models (LLMs)", "NLP"],
                        "resources": [
                            {"name": "LangChain / LlamaIndex Documentation", "url": "https://python.langchain.com/"}
                        ]
                    },
                    {
                        "id": "dl_s3_t2",
                        "title": "Domain Fine-Tuning using LoRA (Low-Rank Adaptation)",
                        "description": "Fine-tune an open-source LLM for a specialized task using Hugging Face PEFT with minimal GPU VRAM.",
                        "skills": ["Neural Networks", "Large Language Models (LLMs)"],
                        "resources": [
                            {"name": "Hugging Face PEFT Documentation", "url": "https://huggingface.co/docs/peft/index"}
                        ]
                    }
                ]
            }
        }
    },

    "full_stack": {
        "id": "full_stack",
        "title": "Full-Stack Development",
        "description": "Engineer responsive user interfaces, robust backend APIs, secure authentication systems, and database workflows.",
        "core_skills": ["HTML", "CSS", "JavaScript", "React", "Backend Development"],
        "potential_roles": ["Full-Stack Developer", "Software Engineer", "Web Application Developer", "Backend Engineer"],
        "roadmap": {
            "stage_1": {
                "name": "Stage 1 – Beginner",
                "summary": "Master core web standards: semantic HTML5, modern CSS layouts, and fundamental JavaScript programming.",
                "tasks": [
                    {
                        "id": "fs_s1_t1",
                        "title": "Semantic HTML5 & Accessible Structure",
                        "description": "Learn semantic elements, forms, accessibility (ARIA), SEO basics, and web page document hierarchy.",
                        "skills": ["HTML"],
                        "resources": [
                            {"name": "freeCodeCamp – Responsive Web Design", "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/"},
                            {"name": "MDN Web Docs – HTML Basics", "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML"}
                        ]
                    },
                    {
                        "id": "fs_s1_t2",
                        "title": "Modern CSS3 (Flexbox, Grid & Responsive Design)",
                        "description": "Master the CSS box model, mobile-first media queries, Flexbox alignment, CSS Grid, and custom variables.",
                        "skills": ["CSS"],
                        "resources": [
                            {"name": "CSS Tricks – Complete Guide to Flexbox", "url": "https://css-tricks.com/snippets/css/a-guide-to-flexbox/"},
                            {"name": "W3Schools CSS Tutorial", "url": "https://www.w3schools.com/css/"}
                        ]
                    },
                    {
                        "id": "fs_s1_t3",
                        "title": "JavaScript Fundamentals & DOM Manipulation",
                        "description": "Master data types, functions, array methods, event listeners, and asynchronous promises.",
                        "skills": ["JavaScript"],
                        "resources": [
                            {"name": "JavaScript.info – Modern JavaScript Tutorial", "url": "https://javascript.info/"},
                            {"name": "freeCodeCamp – JavaScript Algorithms", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/"}
                        ]
                    }
                ]
            },
            "stage_2": {
                "name": "Stage 2 – Intermediate",
                "summary": "Build component-driven frontend applications with React and secure REST APIs with backend frameworks.",
                "tasks": [
                    {
                        "id": "fs_s2_t1",
                        "title": "React Component Architecture & Hooks",
                        "description": "Understand JSX, props, state management with useState/useEffect, event handling, and conditional rendering.",
                        "skills": ["React", "JavaScript"],
                        "resources": [
                            {"name": "React Official Documentation & Tutorial", "url": "https://react.dev/learn"}
                        ]
                    },
                    {
                        "id": "fs_s2_t2",
                        "title": "Backend API Development with Python / Flask",
                        "description": "Build RESTful endpoints, handle JSON payloads, route parameters, status codes, and database CRUD operations.",
                        "skills": ["Backend Development"],
                        "resources": [
                            {"name": "Flask Official Tutorial", "url": "https://flask.palletsprojects.com/en/stable/tutorial/"}
                        ]
                    },
                    {
                        "id": "fs_s2_t3",
                        "title": "Web Security, CSRF, and Authentication",
                        "description": "Implement password hashing, session cookies, CSRF tokens, input validation, and secure HTTP headers.",
                        "skills": ["Backend Development"],
                        "resources": [
                            {"name": "OWASP Top 10 Web Application Security Risks", "url": "https://owasp.org/www-project-top-ten/"}
                        ]
                    }
                ]
            },
            "stage_3": {
                "name": "Stage 3 – Practical Projects",
                "summary": "Ship full-stack web applications with authentication, responsive UI, and persistent databases.",
                "tasks": [
                    {
                        "id": "fs_s3_t1",
                        "title": "Student Collaboration Platform / Task Board",
                        "description": "Create a responsive project management application with user registration, board columns, and real-time task updates.",
                        "skills": ["HTML", "CSS", "JavaScript", "React", "Backend Development"],
                        "resources": [
                            {"name": "MDN – Express and Node / Flask Web Development", "url": "https://developer.mozilla.org/en-US/docs/Learn/Server-side"}
                        ]
                    },
                    {
                        "id": "fs_s3_t2",
                        "title": "Production Deployment & WSGI Configuration",
                        "description": "Deploy an application behind Gunicorn on cloud hosting with environment variables and SQLite/PostgreSQL persistence.",
                        "skills": ["Backend Development"],
                        "resources": [
                            {"name": "Gunicorn Documentation", "url": "https://docs.gunicorn.org/"}
                        ]
                    }
                ]
            }
        }
    }
}

# ============================================================================
# TOP 5 VERIFIED SOURCES RECOMMENDATION (2 Free, 3 Paid) & YOUTUBE BEST RESOURCES
# ============================================================================

VERIFIED_SOURCES = {
    "data_analytics": [
        {
            "name": "freeCodeCamp – Data Analysis with Python Certification",
            "platform": "freeCodeCamp",
            "type": "Free",
            "is_free": True,
            "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/",
            "description": "300 hours of hands-on interactive training in NumPy, Pandas, Matplotlib, Seaborn, and 5 mandatory real-world certification projects.",
            "credential": "Free Verified Certificate"
        },
        {
            "name": "Kaggle Learn – Data Analysis & SQL Micro-Courses",
            "platform": "Kaggle / Google",
            "type": "Free",
            "is_free": True,
            "url": "https://www.kaggle.com/learn",
            "description": "Interactive browser-based labs covering SQL joins, aggregation, data cleaning, and statistical data visualization.",
            "credential": "Free Verified Badges & Certificates"
        },
        {
            "name": "Google Data Analytics Professional Certificate",
            "platform": "Coursera / Google",
            "type": "Paid",
            "is_free": False,
            "url": "https://www.coursera.org/professional-certificates/google-data-analytics",
            "description": "Industry-standard 8-course series covering spreadsheets, SQL database querying, Tableau dashboards, and R programming with capstone case study.",
            "credential": "Google Professional Certificate (Paid / Financial Aid available)"
        },
        {
            "name": "IBM Data Analyst Professional Certificate",
            "platform": "Coursera / IBM",
            "type": "Paid",
            "is_free": False,
            "url": "https://www.coursera.org/professional-certificates/ibm-data-analyst",
            "description": "Comprehensive credential focusing on Python data wrangling, SQL analytics, IBM Cognos dashboards, and business problem solving.",
            "credential": "IBM Professional Certificate (Paid / Financial Aid available)"
        },
        {
            "name": "Microsoft Certified: Power BI Data Analyst Associate (PL-300)",
            "platform": "Microsoft Learn / Pearson VUE",
            "type": "Paid",
            "is_free": False,
            "url": "https://learn.microsoft.com/en-us/credentials/certifications/data-analyst-associate/",
            "description": "Official enterprise certification validating data preparation, DAX modeling, row-level security, and executive reporting in Power BI.",
            "credential": "Microsoft Associate Certification Exam (Paid)"
        }
    ],
    "machine_learning_ai": [
        {
            "name": "fast.ai – Practical Deep Learning & ML for Coders",
            "platform": "fast.ai",
            "type": "Free",
            "is_free": True,
            "url": "https://course.fast.ai/",
            "description": "Acclaimed top-down practical course teaching modern machine learning, PyTorch, computer vision, and tabular data with open Jupyter notebooks.",
            "credential": "Free Open-Source Course"
        },
        {
            "name": "Kaggle Learn – Intro & Intermediate Machine Learning",
            "platform": "Kaggle",
            "type": "Free",
            "is_free": True,
            "url": "https://www.kaggle.com/learn/intro-to-machine-learning",
            "description": "Interactive coding micro-courses covering decision trees, random forests, XGBoost, cross-validation, and feature engineering with instant grading.",
            "credential": "Free Verified Certificate"
        },
        {
            "name": "Machine Learning Specialization by Andrew Ng",
            "platform": "Coursera / DeepLearning.AI & Stanford",
            "type": "Paid",
            "is_free": False,
            "url": "https://www.coursera.org/specializations/machine-learning-introduction",
            "description": "The definitive 3-course foundational masterclass on supervised learning, neural networks, decision trees, and recommender systems.",
            "credential": "Stanford & DeepLearning.AI Certificate (Paid / Financial Aid available)"
        },
        {
            "name": "AWS Certified Machine Learning – Specialty (MLS-C01)",
            "platform": "Amazon Web Services",
            "type": "Paid",
            "is_free": False,
            "url": "https://aws.amazon.com/certification/certified-machine-learning-specialty/",
            "description": "Enterprise cloud credential validating data engineering, ML modeling, hyperparameter optimization, and Amazon SageMaker deployments.",
            "credential": "AWS Specialty Certification Exam (Paid)"
        },
        {
            "name": "Google Cloud Professional Machine Learning Engineer",
            "platform": "Google Cloud Skills Boost",
            "type": "Paid",
            "is_free": False,
            "url": "https://cloud.google.com/learn/certification/machine-learning-engineer",
            "description": "Industry certification for designing scalable ML architectures, Vertex AI training pipelines, and production MLOps monitoring.",
            "credential": "Google Cloud Professional Certification (Paid)"
        }
    ],
    "data_science": [
        {
            "name": "freeCodeCamp – Scientific Computing with Python",
            "platform": "freeCodeCamp",
            "type": "Free",
            "is_free": True,
            "url": "https://www.freecodecamp.org/learn/scientific-computing-with-python/",
            "description": "300 hours of algorithmic problem solving, data structures, and scientific computing projects with rigorous verification.",
            "credential": "Free Verified Certificate"
        },
        {
            "name": "Harvard CS109: Data Science OpenCourseWare",
            "platform": "Harvard University",
            "type": "Free",
            "is_free": True,
            "url": "https://cs109.github.io/2015/",
            "description": "Full Ivy-League college syllabus covering data wrangling, exploratory analysis, regression, classification, clustering, and statistical inference.",
            "credential": "Free University Curriculum"
        },
        {
            "name": "Applied Data Science with Python Specialization",
            "platform": "Coursera / University of Michigan",
            "type": "Paid",
            "is_free": False,
            "url": "https://www.coursera.org/specializations/data-science-python",
            "description": "5-course series covering information visualization, applied machine learning in Python, text mining, and social network analysis.",
            "credential": "University of Michigan Certificate (Paid / Financial Aid available)"
        },
        {
            "name": "IBM Data Science Professional Certificate",
            "platform": "Coursera / IBM",
            "type": "Paid",
            "is_free": False,
            "url": "https://www.coursera.org/professional-certificates/ibm-data-science",
            "description": "10-course industry credential covering data science methodology, Python, SQL, Jupyter, Scikit-learn, and capstone deployment.",
            "credential": "IBM Professional Certificate (Paid / Financial Aid available)"
        },
        {
            "name": "DataCamp – Data Scientist with Python Career Track",
            "platform": "DataCamp",
            "type": "Paid",
            "is_free": False,
            "url": "https://www.datacamp.com/tracks/data-scientist-with-python",
            "description": "Comprehensive interactive track covering statistical simulation, hypothesis testing, machine learning pipelines, and cluster analysis.",
            "credential": "DataCamp Career Track Statement (Paid)"
        }
    ],
    "deep_learning_genai": [
        {
            "name": "Hugging Face Deep Learning & NLP Course",
            "platform": "Hugging Face",
            "type": "Free",
            "is_free": True,
            "url": "https://huggingface.co/learn/nlp-course",
            "description": "Open-source masterclass on Transformers, Tokenizers, Dataset curation, PEFT fine-tuning, and Hugging Face Hub deployment.",
            "credential": "Free Open-Source Course"
        },
        {
            "name": "DeepLearning.AI Short Courses on LLMs & Prompt Engineering",
            "platform": "DeepLearning.AI",
            "type": "Free",
            "is_free": True,
            "url": "https://www.deeplearning.ai/short-courses/",
            "description": "Bite-sized verified courses built with OpenAI, LangChain, and Anthropic covering RAG systems, AI agents, and LLM evaluations.",
            "credential": "Free Verified Courses"
        },
        {
            "name": "Deep Learning Specialization by Andrew Ng",
            "platform": "Coursera / DeepLearning.AI",
            "type": "Paid",
            "is_free": False,
            "url": "https://www.coursera.org/specializations/deep-learning",
            "description": "5 foundational courses covering CNNs, RNNs, LSTM, transformers, hyperparameter tuning, and PyTorch/TensorFlow implementations.",
            "credential": "DeepLearning.AI Certificate (Paid / Financial Aid available)"
        },
        {
            "name": "Generative AI with Large Language Models",
            "platform": "Coursera / DeepLearning.AI & AWS",
            "type": "Paid",
            "is_free": False,
            "url": "https://www.coursera.org/learn/generative-ai-with-llms",
            "description": "Practical enterprise LLM lifecycle: pre-training, instruction fine-tuning (PEFT, LoRA), RLHF, and deployment optimization.",
            "credential": "AWS & DeepLearning.AI Certificate (Paid / Financial Aid available)"
        },
        {
            "name": "NVIDIA Deep Learning Institute (DLI) Fundamentals Certification",
            "platform": "NVIDIA",
            "type": "Paid",
            "is_free": False,
            "url": "https://www.nvidia.com/en-us/training/",
            "description": "Hands-on GPU-accelerated computing and neural network development certification with cloud GPU labs.",
            "credential": "NVIDIA DLI Certificate of Competency (Paid)"
        }
    ],
    "full_stack": [
        {
            "name": "Full Stack Open 2024",
            "platform": "University of Helsinki",
            "type": "Free",
            "is_free": True,
            "url": "https://fullstackopen.com/en/",
            "description": "Renowned university course covering React, Redux, Node.js, Express, MongoDB, GraphQL, TypeScript, and CI/CD with verified certificate.",
            "credential": "Free University Certificate (with ECTS credits available)"
        },
        {
            "name": "freeCodeCamp – Full Stack Web Development Certifications",
            "platform": "freeCodeCamp",
            "type": "Free",
            "is_free": True,
            "url": "https://www.freecodecamp.org/learn",
            "description": "Responsive Web Design, JavaScript Algorithms, and Front End Development Libraries with 15 required portfolio projects.",
            "credential": "Free Verified Certifications"
        },
        {
            "name": "Meta Front-End & Back-End Developer Professional Certificates",
            "platform": "Coursera / Meta",
            "type": "Paid",
            "is_free": False,
            "url": "https://www.coursera.org/professional-certificates/meta-front-end-developer",
            "description": "Dual industry credentials covering HTML, CSS, React, Django, Python, APIs, and relational databases created by Meta engineers.",
            "credential": "Meta Professional Certificate (Paid / Financial Aid available)"
        },
        {
            "name": "The Complete 2024 Web Development Bootcamp by Angela Yu",
            "platform": "Udemy",
            "type": "Paid",
            "is_free": False,
            "url": "https://www.udemy.com/course/the-complete-web-development-bootcamp/",
            "description": "Comprehensive hands-on bootcamp covering modern HTML5, CSS3, JavaScript ES6+, React, Node, Express, and PostgreSQL.",
            "credential": "Certificate of Completion (Paid)"
        },
        {
            "name": "AWS Certified Developer – Associate (DVA-C02)",
            "platform": "Amazon Web Services",
            "type": "Paid",
            "is_free": False,
            "url": "https://aws.amazon.com/certification/certified-developer-associate/",
            "description": "Validates building, deploying, and debugging cloud-native full-stack web applications on AWS serverless and container infrastructure.",
            "credential": "AWS Associate Certification Exam (Paid)"
        }
    ]
}

YOUTUBE_RESOURCES = {
    "data_analytics": [
        {
            "channel": "Alex The Analyst",
            "url": "https://www.youtube.com/@AlexTheAnalyst",
            "focus": "Complete Data Analyst Portfolio Projects, SQL Bootcamps, and Power BI",
            "recommended_playlist": "Full Data Analyst Portfolio Project & SQL Beginner to Advanced"
        },
        {
            "channel": "Luke Barousse",
            "url": "https://www.youtube.com/@LukeBarousse",
            "focus": "Python for Data Analysts, Tableau Dashboards, and Market Skills Analysis",
            "recommended_playlist": "Python for Data Analytics & Real-Time Job Market Insights"
        },
        {
            "channel": "Chandoo",
            "url": "https://www.youtube.com/@chandoo_",
            "focus": "Advanced Excel Dashboards, Power Query, and Power BI Storytelling",
            "recommended_playlist": "Power BI Masterclass & Executive Dashboard Design"
        },
        {
            "channel": "freeCodeCamp.org",
            "url": "https://www.youtube.com/@freecodecamp",
            "focus": "Comprehensive 4-10 Hour Full Courses on SQL, Tableau, and Python Data Analysis",
            "recommended_playlist": "SQL Full Course & Data Analysis with Python Certification"
        }
    ],
    "machine_learning_ai": [
        {
            "channel": "StatQuest with Josh Starmer",
            "url": "https://www.youtube.com/@statquest",
            "focus": "Crystal-Clear Visual Intuition for Regression, Classification, and Neural Nets",
            "recommended_playlist": "Machine Learning Fundamentals & Neural Networks Demystified"
        },
        {
            "channel": "Krish Naik",
            "url": "https://www.youtube.com/@krishnaik06",
            "focus": "End-to-End Machine Learning with Deployment, MLOps, Docker, and CI/CD",
            "recommended_playlist": "Complete Machine Learning Playlist with Real-Time Industry Projects"
        },
        {
            "channel": "Daniel Bourke",
            "url": "https://www.youtube.com/@mrdbourke",
            "focus": "Hands-on PyTorch and TensorFlow Full-Length Coding Bootcamps",
            "recommended_playlist": "Zero to Mastery PyTorch for Deep Learning & Machine Learning Roadmaps"
        },
        {
            "channel": "Sentdex",
            "url": "https://www.youtube.com/@sentdex",
            "focus": "Python Machine Learning and Neural Networks from Scratch",
            "recommended_playlist": "Neural Networks from Scratch in Python (NNFS)"
        }
    ],
    "data_science": [
        {
            "channel": "Ken Jee",
            "url": "https://www.youtube.com/@KenJee_ds",
            "focus": "Data Science Projects from Scratch, Portfolio Optimization, and Industry Advice",
            "recommended_playlist": "Data Science Project from Scratch & Kaggle Competition Strategies"
        },
        {
            "channel": "Keith Galli",
            "url": "https://www.youtube.com/@keithgalli",
            "focus": "Real-World Multi-Million Row Pandas Data Analysis & Project Walkthroughs",
            "recommended_playlist": "Solving Real-World Problems with Python Pandas & Data Science Projects"
        },
        {
            "channel": "CampusX",
            "url": "https://www.youtube.com/@CampusX-official",
            "focus": "In-Depth Mathematics, Statistics, and Python for Data Science Students",
            "recommended_playlist": "100 Days of Machine Learning & Statistics for Data Science"
        },
        {
            "channel": "Data Professor (Chanin Nantasenamat)",
            "url": "https://www.youtube.com/@DataProfessor",
            "focus": "Practical Data Science, Streamlit Web App Deployments, and Bioinformatics",
            "recommended_playlist": "Build Data Science Web Apps with Streamlit & Python"
        }
    ],
    "deep_learning_genai": [
        {
            "channel": "3Blue1Brown",
            "url": "https://www.youtube.com/@3blue1brown",
            "focus": "World-Class Visual Animations of Backpropagation, Attention, and Linear Algebra",
            "recommended_playlist": "Neural Networks & Essence of Linear Algebra"
        },
        {
            "channel": "Andrej Karpathy",
            "url": "https://www.youtube.com/@AndrejKarpathy",
            "focus": "Building GPT from Scratch, micrograd, and Neural Networks: Zero to Hero",
            "recommended_playlist": "Neural Networks: Zero to Hero & nanoGPT Architecture"
        },
        {
            "channel": "AssemblyAI",
            "url": "https://www.youtube.com/@AssemblyAI",
            "focus": "Modern GenAI, LangChain, RAG Systems, Vector Databases, and Speech AI",
            "recommended_playlist": "Building Generative AI Applications & LangChain Crash Courses"
        },
        {
            "channel": "Umar Jamil",
            "url": "https://www.youtube.com/@umarjamilai",
            "focus": "Line-by-Line Code Implementations of Attention, LLaMA, LoRA, and Mistral",
            "recommended_playlist": "Paper Implementations from Scratch: Transformers & Diffusion"
        }
    ],
    "full_stack": [
        {
            "channel": "Traversy Media",
            "url": "https://www.youtube.com/@TraversyMedia",
            "focus": "High-Impact Crash Courses on React, Node.js, Express, REST APIs, and Databases",
            "recommended_playlist": "Modern JavaScript, React, and Full-Stack Project Bootcamps"
        },
        {
            "channel": "Web Dev Simplified",
            "url": "https://www.youtube.com/@WebDevSimplified",
            "focus": "React Hooks, Modern CSS Grid/Flexbox, Async JS, and Clean Architecture",
            "recommended_playlist": "Learn React in 30 Minutes & Full-Stack Authentication"
        },
        {
            "channel": "The Net Ninja",
            "url": "https://www.youtube.com/@NetNinja",
            "focus": "Bite-Sized Modular Playlists on React, Node.js, Express, and TypeScript",
            "recommended_playlist": "Complete React Tutorial & Node.js Crash Course"
        },
        {
            "channel": "Kevin Powell",
            "url": "https://www.youtube.com/@KevinPowell",
            "focus": "Responsive Layouts, Modern CSS Best Practices, and Web Accessibility",
            "recommended_playlist": "CSS Demystified & Responsive Web Design from Scratch"
        }
    ]
}

# Attach verified sources & youtube resources directly to CAREER_DOMAINS metadata
for _k, _dom in CAREER_DOMAINS.items():
    _dom["verified_sources"] = VERIFIED_SOURCES.get(_k, [])
    _dom["youtube_resources"] = YOUTUBE_RESOURCES.get(_k, [])

# Standardized taxonomies for Student Profile
ALL_TECHNICAL_SKILLS = [
    "Python", "SQL", "Statistics", "Power BI",
    "Machine Learning Algorithms", "Mathematics", "Machine Learning",
    "Neural Networks", "NLP", "Large Language Models (LLMs)",
    "HTML", "CSS", "JavaScript", "React", "Backend Development"
]

ALL_INTERESTS = [
    "Data Analysis & Visualization",
    "Business Intelligence & Reporting",
    "Machine Learning & Algorithmic Problem Solving",
    "Mathematical & Statistical Modeling",
    "Scientific Experimentation & Data Science",
    "Deep Learning & Artificial Neural Networks",
    "Generative AI & LLM Applications",
    "Natural Language Processing",
    "Frontend & UI/UX Development",
    "Backend Engineering & Web Security"
]

# Mapping of interests to career domain affinities (used for tie-breaking)
INTEREST_TO_DOMAINS = {
    "Data Analysis & Visualization": ["data_analytics", "data_science"],
    "Business Intelligence & Reporting": ["data_analytics"],
    "Machine Learning & Algorithmic Problem Solving": ["machine_learning_ai", "data_science"],
    "Mathematical & Statistical Modeling": ["machine_learning_ai", "data_science"],
    "Scientific Experimentation & Data Science": ["data_science"],
    "Deep Learning & Artificial Neural Networks": ["deep_learning_genai", "machine_learning_ai"],
    "Generative AI & LLM Applications": ["deep_learning_genai"],
    "Natural Language Processing": ["deep_learning_genai"],
    "Frontend & UI/UX Development": ["full_stack"],
    "Backend Engineering & Web Security": ["full_stack"]
}


# ============================================================================
# 100 ORIGINAL MULTIPLE CHOICE QUESTIONS (20 per domain: 12 Basic, 8 Practical)
# ============================================================================

QUESTIONS = [
    # ------------------------------------------------------------------------
    # 1. DATA ANALYTICS (20 Questions: DA_B01 - DA_B12, DA_P01 - DA_P08)
    # ------------------------------------------------------------------------
    {
        "id": "DA_B01",
        "domain": "data_analytics",
        "type": "basic",
        "question": "In SQL, which clause is specifically used to filter groups of records resulting from a GROUP BY statement?",
        "options": ["WHERE", "HAVING", "ORDER BY", "FILTER"],
        "answer": 1,
        "explanation": "HAVING filters aggregated groups produced by GROUP BY, whereas WHERE filters individual rows before aggregation occurs."
    },
    {
        "id": "DA_B02",
        "domain": "data_analytics",
        "type": "basic",
        "question": "Which metric represents the central value dividing the upper half from the lower half of a sorted data distribution?",
        "options": ["Mean", "Median", "Mode", "Variance"],
        "answer": 1,
        "explanation": "The median is the exact middle observation in a sorted dataset, making it resilient to extreme outliers."
    },
    {
        "id": "DA_B03",
        "domain": "data_analytics",
        "type": "basic",
        "question": "In Microsoft Power BI, what expression language is primarily utilized to write custom calculated columns and dynamic measures?",
        "options": ["DAX (Data Analysis Expressions)", "M Query Language", "VBA Script", "TypeScript"],
        "answer": 0,
        "explanation": "DAX is the formula and query language used in Power BI, Analysis Services, and Power Pivot for analytical calculations."
    },
    {
        "id": "DA_B04",
        "domain": "data_analytics",
        "type": "basic",
        "question": "In Python's pandas library, which method is commonly executed to remove rows containing null or NaN values?",
        "options": ["df.dropna()", "df.clean_nulls()", "df.discard()", "df.remove_nan()"],
        "answer": 0,
        "explanation": "df.dropna() analyzes DataFrame rows or columns and drops those with missing (NaN) values according to threshold parameters."
    },
    {
        "id": "DA_B05",
        "domain": "data_analytics",
        "type": "basic",
        "question": "Which visualization type is most effective for displaying data quartiles, medians, and outliers of a continuous numerical variable?",
        "options": ["Donut Chart", "Box and Whisker Plot", "Stacked Area Chart", "Treemap"],
        "answer": 1,
        "explanation": "A Box Plot explicitly highlights the median, first and third quartiles (IQR), whiskers, and individual statistical outliers."
    },
    {
        "id": "DA_B06",
        "domain": "data_analytics",
        "type": "basic",
        "question": "Which SQL JOIN returns all rows from the primary left table along with matching rows from the right table, filling nulls if unmatched?",
        "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"],
        "answer": 1,
        "explanation": "A LEFT JOIN preserves every row from the left table and matches records from the right table, returning NULLs when no match exists."
    },
    {
        "id": "DA_B07",
        "domain": "data_analytics",
        "type": "basic",
        "question": "In descriptive statistics, what does the standard deviation quantify about a dataset?",
        "options": ["The most frequently occurring observation", "The spread or dispersion of observations around the arithmetic mean", "The total sum of all values divided by two", "The degree of symmetry in a bell curve"],
        "answer": 1,
        "explanation": "Standard deviation measures the average distance that data points deviate from the distribution's arithmetic mean."
    },
    {
        "id": "DA_B08",
        "domain": "data_analytics",
        "type": "basic",
        "question": "Within the Power BI workflow, what is the core role of the Power Query Editor?",
        "options": ["To design 3D animations", "To perform Extract, Transform, and Load (ETL) operations on incoming data sources", "To manage user workspace licenses", "To write neural network models"],
        "answer": 1,
        "explanation": "Power Query connects to diverse data sources to shape, clean, merge, pivot, and transform raw tables prior to analytical modeling."
    },
    {
        "id": "DA_B09",
        "domain": "data_analytics",
        "type": "basic",
        "question": "In pandas, which method allows splitting a DataFrame into groups based on key categories to compute summary metrics like mean or sum?",
        "options": ["df.groupby()", "df.partition()", "df.split_rows()", "df.arrange()"],
        "answer": 0,
        "explanation": "df.groupby() implements the split-apply-combine pattern, enabling aggregations across specific categorical groups."
    },
    {
        "id": "DA_B10",
        "domain": "data_analytics",
        "type": "basic",
        "question": "Which SQL keyword is placed directly after SELECT to filter out duplicate rows from the resulting output?",
        "options": ["UNIQUE", "DISTINCT", "DISCRETE", "SEPARATE"],
        "answer": 1,
        "explanation": "SELECT DISTINCT removes duplicate rows from the query result set so each row returned is unique."
    },
    {
        "id": "DA_B11",
        "domain": "data_analytics",
        "type": "basic",
        "question": "In business intelligence reporting, what does the acronym KPI represent?",
        "options": ["Knowledge Performance Iteration", "Key Performance Indicator", "Kernel Process Interface", "Key Production Index"],
        "answer": 1,
        "explanation": "A Key Performance Indicator (KPI) is a quantifiable measure evaluating how effectively a company achieves key business goals."
    },
    {
        "id": "DA_B12",
        "domain": "data_analytics",
        "type": "basic",
        "question": "If an income dataset contains extreme high values (billionaires in a city survey), which metric best conveys typical resident income?",
        "options": ["Arithmetic Mean", "Median", "Range", "Standard Error"],
        "answer": 1,
        "explanation": "The mean is heavily distorted upwards by high outliers, whereas the median remains stable and reflects true central tendency."
    },
    {
        "id": "DA_P01",
        "domain": "data_analytics",
        "type": "practical",
        "question": "You execute: `SELECT region, SUM(sales) FROM orders GROUP BY region HAVING SUM(sales) > 50000;`. Why would using WHERE instead of HAVING fail?",
        "options": [
            "WHERE cannot evaluate aggregate functions like SUM() because it filters individual rows before grouping occurs",
            "WHERE requires sales to be string data types rather than numerical values",
            "WHERE is only supported in SQLite, not in standard SQL",
            "HAVING is strictly reserved for sorting columns alphabetically"
        ],
        "answer": 0,
        "explanation": "Aggregate expressions like SUM() are computed during grouping; the WHERE clause filters rows prior to the creation of groups."
    },
    {
        "id": "DA_P02",
        "domain": "data_analytics",
        "type": "practical",
        "question": "An analytics audit computes a Pearson correlation of +0.88 between marketing spend and sign-ups. What is the soundest interpretation?",
        "options": [
            "Every dollar spent in marketing is guaranteed to generate exactly 0.88 sign-ups",
            "There is a strong positive linear relationship between marketing spend and sign-ups, though causation requires controlled experimentation",
            "Marketing spend directly caused 88% of all recorded user registrations",
            "The data contains errors because correlation coefficients cannot exceed 0.50"
        ],
        "answer": 1,
        "explanation": "Correlation measures linear association strength between variables, but observational correlation does not directly prove causation."
    },
    {
        "id": "DA_P03",
        "domain": "data_analytics",
        "type": "practical",
        "question": "You merge two DataFrames: `orders` and `customers`. Some orders were placed by guest users who do not exist in `customers`. To keep all orders, which join do you use?",
        "options": [
            "pd.merge(orders, customers, on='cust_id', how='inner')",
            "pd.merge(orders, customers, on='cust_id', how='left')",
            "pd.merge(orders, customers, on='cust_id', how='right')",
            "pd.concat([orders, customers], axis=0)"
        ],
        "answer": 1,
        "explanation": "Using how='left' with orders as the left DataFrame guarantees all order records remain in the merged result."
    },
    {
        "id": "DA_P04",
        "domain": "data_analytics",
        "type": "practical",
        "question": "In a Power BI dashboard, selecting the year '2024' on a slicer turns the Sales metric card blank. What is the most probable data model issue?",
        "options": [
            "The Power BI desktop application file is corrupted and must be reinstalled",
            "The relationship between the Date dimension table and the Sales fact table is inactive or broken, or the Date table lacks 2024 records",
            "The sales column must be changed from numeric currency to text format",
            "Power BI cannot calculate numbers when year filters are applied"
        ],
        "answer": 1,
        "explanation": "Blank visual cards under filter context typically stem from missing keys in the Date dimension or inactive model relationships."
    },
    {
        "id": "DA_P05",
        "domain": "data_analytics",
        "type": "practical",
        "question": "A stakeholder reviews customer service ratings and notes most are 1s and 2s with rare 5s. Which visualization best demonstrates this skewness?",
        "options": [
            "A 3D Pie Chart with slices for each rating",
            "A Frequency Histogram with clear rating bin intervals",
            "A Scatter Plot plotting rating against student roll number",
            "A Radial Gauge Chart with an arbitrary threshold"
        ],
        "answer": 1,
        "explanation": "A Histogram clearly illustrates frequency distribution, modality, and positive or negative skewness across bins."
    },
    {
        "id": "DA_P06",
        "domain": "data_analytics",
        "type": "practical",
        "question": "You need to compute Month-over-Month percentage revenue growth in SQL. Which window function allows you to retrieve the previous row's revenue?",
        "options": [
            "LAG(revenue, 1) OVER (ORDER BY order_month)",
            "LEAD(revenue, 1) OVER (ORDER BY order_month)",
            "FIRST_VALUE(revenue) OVER (PARTITION BY order_month)",
            "NTILE(4) OVER (ORDER BY order_month)"
        ],
        "answer": 0,
        "explanation": "LAG() accesses data from a preceding row at a specified physical offset within the partitioned window."
    },
    {
        "id": "DA_P07",
        "domain": "data_analytics",
        "type": "practical",
        "question": "During data profiling, you discover customer age values of -12, 999, and 'Unknown'. What is the appropriate initial remediation step?",
        "options": [
            "Replace all invalid numbers with zero without notifying stakeholders",
            "Catalog anomalies, replace non-sensical values with appropriate NULL/NaN indicators, and investigate data entry constraints at the source",
            "Delete the entire customer table to prevent calculation errors",
            "Convert the column to a boolean true/false field"
        ],
        "answer": 1,
        "explanation": "Treating obvious data entry errors or sentinel values (like 999) as NULLs preserves data integrity while preventing biased statistical calculations."
    },
    {
        "id": "DA_P08",
        "domain": "data_analytics",
        "type": "practical",
        "question": "An A/B test with 20 visitors per variant yields 60% conversion on A and 40% on B. Why is declaring variant A victorious premature?",
        "options": [
            "Small sample sizes generate wide confidence intervals and high p-values, meaning observed differences are likely random variation",
            "Statistical tests can only evaluate samples larger than 10,000 observations",
            "Conversion rates cannot be expressed as percentages in analytics",
            "Variant B should automatically win if tested on weekends"
        ],
        "answer": 0,
        "explanation": "With tiny sample sizes, the test lacks statistical power, making the observed conversion delta statistically indistinguishable from noise."
    },

    # ------------------------------------------------------------------------
    # 2. MACHINE LEARNING / ARTIFICIAL INTELLIGENCE (20 Questions: ML_B01 - ML_B12, ML_P01 - ML_P08)
    # ------------------------------------------------------------------------
    {
        "id": "ML_B01",
        "domain": "machine_learning_ai",
        "type": "basic",
        "question": "In supervised machine learning, what distinguishes classification from regression tasks?",
        "options": [
            "Classification predicts discrete categorical labels, while regression predicts continuous numerical quantities",
            "Classification requires unlabelled data, whereas regression requires strictly labelled data",
            "Regression is exclusively used for computer vision, while classification is for text",
            "Classification algorithms cannot be evaluated using numeric accuracy metrics"
        ],
        "answer": 0,
        "explanation": "Classification assigns inputs into distinct classes (e.g. spam/ham), while regression forecasts continuous real values (e.g. house prices)."
    },
    {
        "id": "ML_B02",
        "domain": "machine_learning_ai",
        "type": "basic",
        "question": "Which algorithm trains multiple decision trees on random subsets of data and features using bagging (bootstrap aggregation)?",
        "options": ["Random Forest", "Linear Regression", "K-Means Clustering", "Support Vector Machine"],
        "answer": 0,
        "explanation": "Random Forest is an ensemble learning method that constructs numerous decision trees during training and aggregates their votes."
    },
    {
        "id": "ML_B03",
        "domain": "machine_learning_ai",
        "type": "basic",
        "question": "What condition occurs when a machine learning model memorizes training noise and fails to generalize to unseen test instances?",
        "options": ["Underfitting", "Overfitting", "Data Imputation", "Stationarity"],
        "answer": 1,
        "explanation": "Overfitting happens when a model learns the detailed noise of training data so closely that its performance on new, unseen data degrades."
    },
    {
        "id": "ML_B04",
        "domain": "machine_learning_ai",
        "type": "basic",
        "question": "In mathematical optimization, what does the gradient vector of a differentiable loss function point toward?",
        "options": [
            "The direction of steepest rate of increase of the loss function",
            "The exact global minimum coordinate",
            "The average value of the training features",
            "The orthogonal axis perpendicular to all weights"
        ],
        "answer": 0,
        "explanation": "The gradient vector points in the direction of greatest rate of increase; gradient descent therefore steps in the negative gradient direction."
    },
    {
        "id": "ML_B05",
        "domain": "machine_learning_ai",
        "type": "basic",
        "question": "Which classification metric is defined by the formula: True Positives / (True Positives + False Positives)?",
        "options": ["Precision", "Recall (Sensitivity)", "F1 Score", "Specificity"],
        "answer": 0,
        "explanation": "Precision answers: 'Out of all items predicted as positive, how many were truly positive?'"
    },
    {
        "id": "ML_B06",
        "domain": "machine_learning_ai",
        "type": "basic",
        "question": "K-Means is a canonical example of which machine learning paradigm?",
        "options": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Imitation Learning"],
        "answer": 1,
        "explanation": "K-Means clusters unlabeled observations into k groups based on geometric proximity to centroids without supervision."
    },
    {
        "id": "ML_B07",
        "domain": "machine_learning_ai",
        "type": "basic",
        "question": "What is the primary role of an independent test dataset in model evaluation?",
        "options": [
            "To calibrate the internal model weights during backpropagation",
            "To provide an unbiased assessment of the final model's generalization performance on unseen real-world data",
            "To double the number of samples available for hyperparameter tuning",
            "To replace missing values in the training set"
        ],
        "answer": 1,
        "explanation": "The test set must remain completely unseen during training and tuning to provide an honest estimate of generalization error."
    },
    {
        "id": "ML_B08",
        "domain": "machine_learning_ai",
        "type": "basic",
        "question": "In gradient descent algorithms, what does the hyperparameter 'learning rate' (alpha) control?",
        "options": [
            "The number of features randomly selected at each split",
            "The step size taken along the negative gradient direction during parameter updates",
            "The percentage of data assigned to the training split",
            "The regularizer penalty applied to linear intercepts"
        ],
        "answer": 1,
        "explanation": "Learning rate controls the magnitude of parameter adjustments in the negative gradient direction on each iteration."
    },
    {
        "id": "ML_B09",
        "domain": "machine_learning_ai",
        "type": "basic",
        "question": "Which linear algebra operation is foundational to calculating forward projections and weighted inputs in machine learning models?",
        "options": ["Matrix multiplication / Dot product", "String concatenation", "Bitwise AND", "Scalar modulus"],
        "answer": 0,
        "explanation": "Matrix dot products compute linear combinations of feature vectors and weight matrices across all linear and neural models."
    },
    {
        "id": "ML_B10",
        "domain": "machine_learning_ai",
        "type": "basic",
        "question": "In the Python scikit-learn library, what method is invoked to train a model on training feature matrices and targets?",
        "options": [".predict()", ".fit()", ".train()", ".execute()"],
        "answer": 1,
        "explanation": "In scikit-learn's standard API, the .fit(X, y) method estimates model parameters from the supplied training data."
    },
    {
        "id": "ML_B11",
        "domain": "machine_learning_ai",
        "type": "basic",
        "question": "Despite having 'regression' in its name, what primary task does Logistic Regression perform?",
        "options": [
            "Binary or multiclass classification by modeling class probabilities via the sigmoid/logistic function",
            "Unsupervised clustering of point clouds",
            "Continuous stock price prediction without bounds",
            "Dimensionality reduction of image channels"
        ],
        "answer": 0,
        "explanation": "Logistic regression maps linear combinations of features through the sigmoid function to predict category probabilities for classification."
    },
    {
        "id": "ML_B12",
        "domain": "machine_learning_ai",
        "type": "basic",
        "question": "What is the primary benefit of L2 Regularization (Ridge) in linear and machine learning models?",
        "options": [
            "It forces all feature weights to become exactly zero",
            "It penalizes large weight coefficients to prevent overfitting and control model complexity",
            "It eliminates the need for data normalization",
            "It guarantees zero training error"
        ],
        "answer": 1,
        "explanation": "Ridge regularization adds a penalty proportional to the sum of squared weights, shrinking coefficients and reducing model variance."
    },
    {
        "id": "ML_P01",
        "domain": "machine_learning_ai",
        "type": "practical",
        "question": "A financial fraud classifier achieves 99.8% raw accuracy on a dataset where 0.2% of transactions are fraudulent. Why might this model be worthless?",
        "options": [
            "A trivial baseline model predicting 'no fraud' for all records scores 99.8% accuracy while catching 0% of actual fraud",
            "Accuracy cannot be calculated on decimal percentages",
            "Fraud detection algorithms are only permitted to use regression formulas",
            "Accuracy metrics are mathematically invalid for binary labels"
        ],
        "answer": 0,
        "explanation": "Under extreme class imbalance, a naive majority-class predictor gets high accuracy while missing all minority positive cases; Recall and PR-AUC are vital."
    },
    {
        "id": "ML_P02",
        "domain": "machine_learning_ai",
        "type": "practical",
        "question": "You train a Decision Tree with no depth limit and observe 100% training accuracy but 59% test accuracy. What is the most effective immediate remedy?",
        "options": [
            "Increase the tree's maximum depth and number of leaves",
            "Regularize by setting max_depth, min_samples_split, or switching to an ensemble like Random Forest",
            "Duplicate the training data records ten times",
            "Remove all categorical features from the dataset"
        ],
        "answer": 1,
        "explanation": "An unconstrained tree overfits by creating leaves for individual data points. Constraining depth or using bagging combats overfitting."
    },
    {
        "id": "ML_P03",
        "domain": "machine_learning_ai",
        "type": "practical",
        "question": "You feed two features into a Support Vector Machine (SVM): Age (18–80) and Annual Income ($20,000–$500,000). Why is feature scaling essential?",
        "options": [
            "SVM distance calculations (e.g. Euclidean distances in RBF kernels) will be overwhelmed by the large numerical scale of Income",
            "SVM algorithms automatically crash if numbers exceed 100",
            "Income values cannot be multiplied by floating-point numbers",
            "Scaling prevents the target labels from flipping sign"
        ],
        "answer": 0,
        "explanation": "Distance-based algorithms (SVM, KNN, K-Means) compute vector distances; without scaling, large-magnitude features completely dominate the objective."
    },
    {
        "id": "ML_P04",
        "domain": "machine_learning_ai",
        "type": "practical",
        "question": "Your model displays high training error and equally high validation error (high bias / underfitting). Which intervention is most appropriate?",
        "options": [
            "Increase model complexity (e.g., add polynomial features, deepen trees, reduce regularization penalties)",
            "Discard half the features and apply heavy L1 penalties",
            "Decrease the number of training iterations to stop early",
            "Collect fewer training samples to simplify the problem"
        ],
        "answer": 0,
        "explanation": "High bias means the model is too simplistic to capture the true underlying data patterns; increasing capacity or features helps reduce bias."
    },
    {
        "id": "ML_P05",
        "domain": "machine_learning_ai",
        "type": "practical",
        "question": "In 5-fold cross-validation, how is the training and evaluation executed across iterations?",
        "options": [
            "The dataset is divided into 5 equal folds; the model is trained 5 times, using 4 folds for training and 1 fold for validation in each iteration",
            "The model is evaluated only on 5 random rows chosen from the entire dataset",
            "Five separate models are trained on the same data with 5 different learning rates",
            "The dataset is cloned 5 times to simulate large data"
        ],
        "answer": 0,
        "explanation": "K-fold cross-validation rotates through k partitions so every single observation serves in the validation fold exactly once."
    },
    {
        "id": "ML_P06",
        "domain": "machine_learning_ai",
        "type": "practical",
        "question": "In a clinical cancer screening tool, failing to diagnose a sick patient (False Negative) has critical consequences. Which metric should be prioritized?",
        "options": [
            "Recall (Sensitivity)",
            "Precision",
            "Specificity",
            "Negative Predictive Value exclusively"
        ],
        "answer": 0,
        "explanation": "Recall measures the proportion of actual positives correctly identified; maximizing recall minimizes dangerous False Negatives."
    },
    {
        "id": "ML_P07",
        "domain": "machine_learning_ai",
        "type": "practical",
        "question": "During model optimization with gradient descent, the loss function oscillates wildly between large positive numbers and diverges. What is the cause?",
        "options": [
            "The learning rate is set too high, causing parameter updates to overshoot the minimum",
            "The dataset has too many training epochs",
            "The loss function is strictly convex",
            "The weights were initialized to zero"
        ],
        "answer": 0,
        "explanation": "An excessively large learning rate causes gradient updates to step past the valley and overshoot, leading to oscillation and divergence."
    },
    {
        "id": "ML_P08",
        "domain": "machine_learning_ai",
        "type": "practical",
        "question": "When computing Principal Component Analysis (PCA) on a standardized feature matrix, what do the calculated eigenvectors indicate?",
        "options": [
            "The orthogonal directions of maximum variance within the multi-dimensional feature space",
            "The cluster centroid coordinates for K-Means",
            "The misclassified instances from the training set",
            "The learning rate trajectory of the optimizer"
        ],
        "answer": 0,
        "explanation": "Eigenvectors of the feature covariance matrix define the principal axes along which data points exhibit the greatest variance."
    },

    # ------------------------------------------------------------------------
    # 3. DATA SCIENCE (20 Questions: DS_B01 - DS_B12, DS_P01 - DS_P08)
    # ------------------------------------------------------------------------
    {
        "id": "DS_B01",
        "domain": "data_science",
        "type": "basic",
        "question": "What is the primary objective of Exploratory Data Analysis (EDA) in a data science project?",
        "options": [
            "To deploy machine learning models directly into production clusters",
            "To uncover patterns, distributions, correlations, and anomalies to inform subsequent modeling decisions",
            "To compile HTML templates for frontend user forms",
            "To write automated unit tests for web APIs"
        ],
        "answer": 1,
        "explanation": "EDA allows practitioners to visually and statistically inspect data characteristics and uncover hidden structures prior to modeling."
    },
    {
        "id": "DS_B02",
        "domain": "data_science",
        "type": "basic",
        "question": "Which Python library provides high-performance n-dimensional array objects and vectorized mathematical routines as the foundation of data science?",
        "options": ["NumPy", "Jinja2", "Requests", "Werkzeug"],
        "answer": 0,
        "explanation": "NumPy provides the fundamental ndarray object and optimized C-speed vectorized mathematical operations."
    },
    {
        "id": "DS_B03",
        "domain": "data_science",
        "type": "basic",
        "question": "In statistical hypothesis testing, what conclusion is drawn when a computed p-value is less than the predetermined significance level alpha (e.g. 0.05)?",
        "options": [
            "Reject the null hypothesis; the observed evidence is statistically significant",
            "Accept the null hypothesis as proven truth",
            "The experiment is flawed and must be discarded entirely",
            "The sample size must be multiplied by two"
        ],
        "answer": 0,
        "explanation": "A p-value < alpha provides sufficient empirical evidence to reject the null hypothesis in favor of the alternative hypothesis."
    },
    {
        "id": "DS_B04",
        "domain": "data_science",
        "type": "basic",
        "question": "Which data transformation converts a categorical column with N levels into N separate binary (0 or 1) indicator columns?",
        "options": ["One-Hot Encoding", "Min-Max Normalization", "Box-Cox Transformation", "Label Binarizer Matrix"],
        "answer": 0,
        "explanation": "One-Hot Encoding creates binary dummy columns for each categorical level, enabling numerical algorithms to process non-ordinal categories."
    },
    {
        "id": "DS_B05",
        "domain": "data_science",
        "type": "basic",
        "question": "What is the purpose of computing a feature correlation matrix before training a regression model?",
        "options": [
            "To identify pairwise linear relationships and diagnose potential multicollinearity between predictors",
            "To sort all rows in ascending order",
            "To encrypt student personal records",
            "To automatically remove rows with missing data"
        ],
        "answer": 0,
        "explanation": "A correlation matrix reveals strong linear dependencies between features, alerting the scientist to multicollinearity."
    },
    {
        "id": "DS_B06",
        "domain": "data_science",
        "type": "basic",
        "question": "According to the Central Limit Theorem, what happens to the distribution of sample means as the sample size (n) becomes sufficiently large?",
        "options": [
            "It approaches a normal (Gaussian) distribution, regardless of the underlying population's original shape",
            "It turns completely uniform across all numbers",
            "The standard deviation increases exponentially",
            "The mean automatically becomes equal to 1"
        ],
        "answer": 0,
        "explanation": "The CLT states that sums and means of independent random variables tend toward a normal distribution as sample size grows."
    },
    {
        "id": "DS_B07",
        "domain": "data_science",
        "type": "basic",
        "question": "In SQL, which aggregate function returns the total count of non-null entries for a designated column?",
        "options": ["COUNT(column_name)", "SUM_ROWS()", "TOTAL()", "INDEX_COUNT()"],
        "answer": 0,
        "explanation": "COUNT(column_name) tallies all rows containing non-null values for the specified column."
    },
    {
        "id": "DS_B08",
        "domain": "data_science",
        "type": "basic",
        "question": "What does the term 'data leakage' describe in predictive modeling?",
        "options": [
            "Information from outside the training dataset (such as target values from validation/test data) inadvertently enters model training",
            "A security breach exposing proprietary data onto the internet",
            "Loss of data due to disk drive corruption",
            "Memory leak caused by unclosed file pointers"
        ],
        "answer": 0,
        "explanation": "Data leakage occurs when target information or future knowledge is inadvertently included in training features, producing unrealistically high validation scores."
    },
    {
        "id": "DS_B09",
        "domain": "data_science",
        "type": "basic",
        "question": "Which Python library builds on top of Matplotlib to provide high-level, aesthetically pleasing statistical graphics such as heatmaps and violin plots?",
        "options": ["Seaborn", "Pygame", "BeautifulSoup", "Twisted"],
        "answer": 0,
        "explanation": "Seaborn is a specialized Python statistical data visualization library built directly upon Matplotlib and integrated with pandas."
    },
    {
        "id": "DS_B10",
        "domain": "data_science",
        "type": "basic",
        "question": "In data preprocessing, what does the technique of 'imputation' entail?",
        "options": [
            "Substituting missing or unobserved values with statistically estimated values like mean, median, or modeled predictions",
            "Deleting all numerical columns from the dataset",
            "Hashing passwords before database storage",
            "Reordering columns alphabetically"
        ],
        "answer": 0,
        "explanation": "Imputation fills missing data points using estimated values, preventing loss of sample volume associated with listwise deletion."
    },
    {
        "id": "DS_B11",
        "domain": "data_science",
        "type": "basic",
        "question": "In statistical hypothesis testing, what constitutes a Type I error?",
        "options": [
            "A false positive: rejecting a true null hypothesis when no actual effect exists",
            "A false negative: failing to reject a false null hypothesis",
            "A mathematical division by zero in calculations",
            "A sample size that is too large"
        ],
        "answer": 0,
        "explanation": "A Type I error is a false alarm (false positive) where researchers incorrectly reject a null hypothesis that was actually true."
    },
    {
        "id": "DS_B12",
        "domain": "data_science",
        "type": "basic",
        "question": "What is the primary role of a pipeline object (e.g. scikit-learn Pipeline) in data science workflows?",
        "options": [
            "To encapsulate sequential transformations (imputation, scaling) and estimators into a single reproducible, leakage-free object",
            "To stream audio files across network protocols",
            "To compress database tables into ZIP archives",
            "To render CSS flexbox layouts"
        ],
        "answer": 0,
        "explanation": "Pipelines bundle preprocessing and model training steps together, guaranteeing transformations fit strictly on training splits."
    },
    {
        "id": "DS_P01",
        "domain": "data_science",
        "type": "practical",
        "question": "A developer calculates the mean of a feature using the entire dataset (train + test together) to impute missing values before splitting. Why is this problematic?",
        "options": [
            "It introduces data leakage by incorporating test set information into the training process, leading to over-optimistic performance metrics",
            "The mean cannot be calculated when test data exists",
            "pandas throws a fatal exception when computing means before train_test_split",
            "Imputation must strictly use the geometric mean rather than the arithmetic mean"
        ],
        "answer": 0,
        "explanation": "Computing statistics on the full dataset before splitting leaks test distribution information into the training pipeline."
    },
    {
        "id": "DS_P02",
        "domain": "data_science",
        "type": "practical",
        "question": "A survey of student monthly expenses shows 98% spend between $100 and $400, while two students spend $250,000. Which summary statistic best conveys typical expenditure?",
        "options": [
            "The Median",
            "The Arithmetic Mean",
            "The Sample Range",
            "The Standard Error of the Mean"
        ],
        "answer": 0,
        "explanation": "The median represents the 50th percentile and remains unaffected by extreme outliers that severely distort the arithmetic mean."
    },
    {
        "id": "DS_P03",
        "domain": "data_science",
        "type": "practical",
        "question": "You conduct an A/B test to test if a new homepage layout improves the click-through rate (CTR) proportion from 8% to 11%. Which test is appropriate?",
        "options": [
            "Two-sample z-test or Chi-square test for comparing independent proportions",
            "One-way ANOVA for comparing multiple continuous means",
            "K-Means clustering algorithm",
            "Principal Component Analysis"
        ],
        "answer": 0,
        "explanation": "Comparing binomial conversion proportions between two randomized independent groups is evaluated with a two-proportion z-test or chi-square test."
    },
    {
        "id": "DS_P04",
        "domain": "data_science",
        "type": "practical",
        "question": "In SQL, you must rank customers by total spend within each geographical country and select only the top 3 per country. Which syntax achieves this cleanly?",
        "options": [
            "Use DENSE_RANK() OVER (PARTITION BY country ORDER BY total_spend DESC) within a CTE or subquery, filtering where rank <= 3",
            "Execute a simple WHERE total_spend > 3 without grouping",
            "Run a CROSS JOIN between customer and country tables",
            "Use GROUP BY country HAVING total_spend <= 3"
        ],
        "answer": 0,
        "explanation": "Window ranking functions with PARTITION BY country enable ranking within subgroups; filtering the rank in an outer query retrieves top records."
    },
    {
        "id": "DS_P05",
        "domain": "data_science",
        "type": "practical",
        "question": "You have a categorical variable 'Zip_Code' with 15,000 distinct values. Why is standard One-Hot Encoding ill-advised here?",
        "options": [
            "It produces 15,000 sparse columns, causing massive memory explosion and the curse of dimensionality",
            "One-Hot Encoding is mathematically forbidden on geographical numbers",
            "Zip codes cannot be processed in Python arrays",
            "It changes all target values to zero"
        ],
        "answer": 0,
        "explanation": "High-cardinality features cause extreme memory blowup and severe sparsity when one-hot encoded; target encoding or frequency encoding is preferable."
    },
    {
        "id": "DS_P06",
        "domain": "data_science",
        "type": "practical",
        "question": "When plotting the residuals of a linear regression model against predicted values, you observe a prominent parabolic (U-shaped) curve. What does this reveal?",
        "options": [
            "The true relationship between predictors and response is non-linear, violating the linear assumption",
            "The model is mathematically perfect with zero residual variance",
            "The target variable must be converted to binary boolean labels",
            "The residual plot indicates perfect homoscedasticity"
        ],
        "answer": 0,
        "explanation": "Residuals from a sound linear model should exhibit random scatter; systematic curvature reveals uncaptured non-linear relationships."
    },
    {
        "id": "DS_P07",
        "domain": "data_science",
        "type": "practical",
        "question": "Two independent variables in your multiple regression model have a pairwise correlation of r = 0.99. What statistical risk does this present?",
        "options": [
            "Severe multicollinearity, resulting in unstable coefficient estimates and inflated standard errors",
            "The model's R-squared value will automatically drop to zero",
            "The regression line will fail to compute any intercept",
            "It guarantees 100% predictive accuracy on test data"
        ],
        "answer": 0,
        "explanation": "Multicollinearity inflates coefficient variance, making it impossible to isolate the individual impact of correlated features on the target."
    },
    {
        "id": "DS_P08",
        "domain": "data_science",
        "type": "practical",
        "question": "When presenting data science findings to executive business stakeholders, which communication approach is most impactful?",
        "options": [
            "Communicate actionable insights, business trade-offs, financial impact, and clear visuals rather than raw algorithmic mathematical equations",
            "Display 500 lines of unformatted Python terminal logs",
            "Refuse to explain predictions unless stakeholders learn linear algebra",
            "Only present the model's hyperparameter tuning grid search table"
        ],
        "answer": 0,
        "explanation": "Effective data scientists translate statistical models into tangible business value, risk assessments, and actionable recommendations."
    },

    # ------------------------------------------------------------------------
    # 4. DEEP LEARNING / GENERATIVE AI (20 Questions: DL_B01 - DL_B12, DL_P01 - DL_P08)
    # ------------------------------------------------------------------------
    {
        "id": "DL_B01",
        "domain": "deep_learning_genai",
        "type": "basic",
        "question": "What is the primary mathematical purpose of applying non-linear activation functions (e.g. ReLU, GELU) in neural networks?",
        "options": [
            "They allow the network to learn complex, non-linear function mappings beyond linear matrix transformations",
            "They compress the model size on disk",
            "They eliminate the need for backward propagation passes",
            "They convert floating point numbers into integers"
        ],
        "answer": 0,
        "explanation": "Without non-linear activations, composing multiple linear layers remains equivalent to a single linear transformation."
    },
    {
        "id": "DL_B02",
        "domain": "deep_learning_genai",
        "type": "basic",
        "question": "Which algorithm computes the partial derivatives of the loss with respect to all network weights using the calculus chain rule?",
        "options": ["Backpropagation", "Breadth-First Search", "Dijkstra's Algorithm", "Binary Search"],
        "answer": 0,
        "explanation": "Backpropagation applies the calculus chain rule backward from output to input layers to compute gradients for optimization."
    },
    {
        "id": "DL_B03",
        "domain": "deep_learning_genai",
        "type": "basic",
        "question": "In Natural Language Processing (NLP), what is the process of breaking down raw text strings into discrete atomic units called?",
        "options": ["Tokenization", "Quantization", "Vectorization", "Distillation"],
        "answer": 0,
        "explanation": "Tokenization converts raw character strings into discrete tokens (words, subwords, or characters) indexed in a model vocabulary."
    },
    {
        "id": "DL_B04",
        "domain": "deep_learning_genai",
        "type": "basic",
        "question": "Which architecture introduced the multi-head self-attention mechanism in the seminal 2017 paper 'Attention Is All You Need'?",
        "options": ["Transformer", "Convolutional Neural Network (CNN)", "Recurrent Neural Network (RNN)", "Restricted Boltzmann Machine"],
        "answer": 0,
        "explanation": "The Transformer architecture replaced recurrence with multi-head self-attention, enabling parallel training over sequence contexts."
    },
    {
        "id": "DL_B05",
        "domain": "deep_learning_genai",
        "type": "basic",
        "question": "What does the 'Dropout' regularization technique do during training forward passes in deep neural networks?",
        "options": [
            "Randomly sets a specified fraction of neuron activations to zero to prevent complex co-adaptations",
            "Permanently deletes unpromising layers from the architecture",
            "Halts training if the loss function dips below a threshold",
            "Removes duplicate records from training batches"
        ],
        "answer": 0,
        "explanation": "Dropout randomly deactivates neurons during each training step, forcing the network to learn robust, distributed representations."
    },
    {
        "id": "DL_B06",
        "domain": "deep_learning_genai",
        "type": "basic",
        "question": "What is an autoregressive Large Language Model (like GPT) primarily trained to do during pre-training?",
        "options": [
            "Predict the next token in a sequence given the preceding context tokens",
            "Classify whether an SQL query contains syntax errors",
            "Compile Python scripts into machine bytecodes",
            "Render 3D graphic models from text specifications"
        ],
        "answer": 0,
        "explanation": "Autoregressive LLMs undergo causal language modeling, optimizing cross-entropy loss to predict the next token across extensive text datasets."
    },
    {
        "id": "DL_B07",
        "domain": "deep_learning_genai",
        "type": "basic",
        "question": "In Generative AI and LLMs, what does the term 'Hallucination' specifically denote?",
        "options": [
            "When the model outputs fluent, grammatically confident assertions that are factually ungrounded or untrue",
            "When the GPU runs out of VRAM memory during inference",
            "When a prompt exceeds the maximum context window length",
            "When user prompts contain emoji characters"
        ],
        "answer": 0,
        "explanation": "Hallucination describes generative text that sounds persuasive and authoritative but contradicts reality or source context."
    },
    {
        "id": "DL_B08",
        "domain": "deep_learning_genai",
        "type": "basic",
        "question": "What does 'Prompt Engineering' encompass in modern AI application development?",
        "options": [
            "Designing, structuring, and optimizing natural language inputs and few-shot examples to elicit desired model behaviors",
            "Soldering physical integrated circuit chips",
            "Writing low-level CUDA kernels for GPU parallelism",
            "Formatting database table indices"
        ],
        "answer": 0,
        "explanation": "Prompt engineering involves structuring instructions, context, constraints, and examples to guide LLM outputs reliably."
    },
    {
        "id": "DL_B09",
        "domain": "deep_learning_genai",
        "type": "basic",
        "question": "Which loss function is universally utilized to train multi-class neural networks featuring a Softmax output layer?",
        "options": ["Categorical Cross-Entropy", "Mean Squared Error (MSE)", "Mean Absolute Error (MAE)", "Huber Loss"],
        "answer": 0,
        "explanation": "Categorical Cross-Entropy measures the distance between predicted probability distributions (via Softmax) and one-hot true labels."
    },
    {
        "id": "DL_B10",
        "domain": "deep_learning_genai",
        "type": "basic",
        "question": "What is Transfer Learning in the context of deep learning and computer vision / NLP?",
        "options": [
            "Taking a model pre-trained on a massive corpus and fine-tuning its weights on a smaller, task-specific dataset",
            "Transferring training scripts over an FTP server",
            "Converting a Python script into C++ code",
            "Moving data from CPU RAM into GPU VRAM"
        ],
        "answer": 0,
        "explanation": "Transfer learning leverages learned representations from large datasets to achieve superior performance on smaller target tasks."
    },
    {
        "id": "DL_B11",
        "domain": "deep_learning_genai",
        "type": "basic",
        "question": "What does the acronym RAG represent in modern Generative AI application architectures?",
        "options": [
            "Retrieval-Augmented Generation",
            "Recurrent Attention Gate",
            "Random Array Gradient",
            "Residual Autoencoding Graph"
        ],
        "answer": 0,
        "explanation": "Retrieval-Augmented Generation (RAG) fetches relevant external knowledge chunks and injects them into the LLM context prompt."
    },
    {
        "id": "DL_B12",
        "domain": "deep_learning_genai",
        "type": "basic",
        "question": "Why do Transformer architectures require explicit Positional Encodings added to input token embeddings?",
        "options": [
            "Because pure self-attention operations are permutation-invariant and cannot discern word ordering without positional cues",
            "To encrypt sensitive words before attention computation",
            "To speed up GPU matrix calculations",
            "To compress the vocabulary size"
        ],
        "answer": 0,
        "explanation": "Self-attention computes token-to-token dot products irrespective of sequence position; positional encodings inject order information."
    },
    {
        "id": "DL_P01",
        "domain": "deep_learning_genai",
        "type": "practical",
        "question": "While training a 40-layer deep feedforward network with Sigmoid activation functions, weights in the earliest layers stop updating. What occurred?",
        "options": [
            "The Vanishing Gradient problem: repeated chain rule multiplication of small sigmoid derivatives (< 0.25) decayed gradients to near-zero",
            "The Exploding Gradient problem: numbers overflowed 64-bit precision",
            "The network reached global zero loss on epoch one",
            "The learning rate was multiplied by ten automatically"
        ],
        "answer": 0,
        "explanation": "Sigmoid derivatives have a maximum value of 0.25; chaining them through deep layers causes gradients to vanish exponentially."
    },
    {
        "id": "DL_P02",
        "domain": "deep_learning_genai",
        "type": "practical",
        "question": "How does the ReLU activation function, f(x) = max(0, x), resolve the vanishing gradient issue for positive inputs?",
        "options": [
            "Its derivative is identically 1 for all positive inputs, allowing gradient signals to backpropagate without diminishing",
            "It squashes all numbers into the range between -1 and +1",
            "It eliminates negative numbers before the dataset is loaded",
            "It automatically recalculates batch normalization parameters"
        ],
        "answer": 0,
        "explanation": "With a constant derivative of 1 for x > 0, ReLU allows gradients to propagate backward through many layers without exponential decay."
    },
    {
        "id": "DL_P03",
        "domain": "deep_learning_genai",
        "type": "practical",
        "question": "You must create a question-answering assistant over proprietary internal college policy documents that are revised weekly. What architecture is ideal?",
        "options": [
            "A Retrieval-Augmented Generation (RAG) pipeline querying chunked document embeddings stored in a vector database",
            "Re-training a 70-billion parameter foundation LLM from scratch every single weekend",
            "Hardcoding all college rules into thousands of static if-else statements",
            "Using a simple regular expression keyword finder without language models"
        ],
        "answer": 0,
        "explanation": "RAG enables dynamic grounding of queries against frequently updated internal documents without costly continuous model retraining."
    },
    {
        "id": "DL_P04",
        "domain": "deep_learning_genai",
        "type": "practical",
        "question": "During neural training, training loss steadily drops to 0.04 while validation loss bottoms at 0.35 and steadily climbs to 0.95. What action is required?",
        "options": [
            "Apply Early Stopping, increase dropout, or introduce weight decay because the network is severely overfitting",
            "Continue training for 200 more epochs at a higher learning rate",
            "Delete the validation dataset because it is misleading the model",
            "Remove all activation functions from the hidden layers"
        ],
        "answer": 0,
        "explanation": "A divergence between falling training loss and rising validation loss is the hallmark of overfitting; early stopping recovers the best checkpoint."
    },
    {
        "id": "DL_P05",
        "domain": "deep_learning_genai",
        "type": "practical",
        "question": "When configuring an LLM for structured code generation or factual data extraction, how should the 'temperature' parameter be tuned?",
        "options": [
            "Set temperature to a low value (e.g. 0.0 to 0.2) to make token selection deterministic and focused",
            "Set temperature to 1.8 to encourage maximum random token exploration",
            "Set temperature to negative numbers to accelerate response speed",
            "Temperature has no mathematical effect on token sampling"
        ],
        "answer": 0,
        "explanation": "Lower temperatures sharpen the softmax probability distribution over vocabulary logits, yielding consistent, deterministic outputs."
    },
    {
        "id": "DL_P06",
        "domain": "deep_learning_genai",
        "type": "practical",
        "question": "You are building a semantic search engine to match student queries with library textbook passages. What approach captures true contextual meaning?",
        "options": [
            "Encode both query and passages into dense vector embeddings using a pre-trained transformer and measure cosine similarity",
            "Count the exact number of matching characters between query and passage",
            "Compare the alphabetical order of first words",
            "Sort passages by file size on the hard drive"
        ],
        "answer": 0,
        "explanation": "Transformer embedding models capture semantic context in dense vector spaces, where cosine similarity measures conceptual closeness."
    },
    {
        "id": "DL_P07",
        "domain": "deep_learning_genai",
        "type": "practical",
        "question": "You wish to adapt an open-source 8B parameter LLM to medical terminology on a single consumer GPU. Which Parameter-Efficient Fine-Tuning (PEFT) method applies?",
        "options": [
            "LoRA (Low-Rank Adaptation), which freezes base model weights and trains small low-rank decomposition rank matrices",
            "Full parameter fine-tuning of all 8 billion parameters in FP32 precision",
            "Genetic algorithm mutation of all transformer attention layers",
            "Deleting 50% of the transformer layers randomly"
        ],
        "answer": 0,
        "explanation": "LoRA injects trainable low-rank decomposition matrices into attention weights, reducing trainable parameters and VRAM requirements by over 90%."
    },
    {
        "id": "DL_P08",
        "domain": "deep_learning_genai",
        "type": "practical",
        "question": "In a RAG system, text chunking creates chunks that split sentences mid-thought, degrading retrieved context. What chunking strategy mitigates this?",
        "options": [
            "Recursive character text splitting with appropriate chunk size and generous chunk overlap (e.g. 100-200 tokens)",
            "Splitting strictly every 10 characters regardless of punctuation",
            "Storing the entire 400-page book in one single chunk",
            "Disabling text chunking and indexing only chapter titles"
        ],
        "answer": 0,
        "explanation": "Recursive splitting respects natural structural boundaries (paragraphs, sentences) and chunk overlap preserves boundary context."
    },

    # ------------------------------------------------------------------------
    # 5. FULL-STACK DEVELOPMENT (20 Questions: FS_B01 - FS_B12, FS_P01 - FS_P08)
    # ------------------------------------------------------------------------
    {
        "id": "FS_B01",
        "domain": "full_stack",
        "type": "basic",
        "question": "What does the practice of writing 'semantic HTML' mean in modern web engineering?",
        "options": [
            "Using HTML tags that describe the meaning and role of content (e.g. <header>, <nav>, <article>, <main>) rather than generic <div> tags",
            "Applying inline CSS styling to every single HTML element",
            "Writing backend Python code directly inside HTML attributes",
            "Minifying HTML files to a single continuous line"
        ],
        "answer": 0,
        "explanation": "Semantic tags convey the structural purpose of document elements to browsers, screen readers, search engines, and developers."
    },
    {
        "id": "FS_B02",
        "domain": "full_stack",
        "type": "basic",
        "question": "What is the CSS Box Model composed of, ordered from the innermost layer to the outermost perimeter?",
        "options": [
            "Content, Padding, Border, Margin",
            "Margin, Border, Padding, Content",
            "Border, Margin, Padding, Content",
            "Padding, Content, Margin, Border"
        ],
        "answer": 0,
        "explanation": "The standard box model consists of the core Content, surrounding Padding, enclosing Border, and outermost Margin."
    },
    {
        "id": "FS_B03",
        "domain": "full_stack",
        "type": "basic",
        "question": "In JavaScript, what is the key difference between the loose equality operator (==) and strict equality operator (===)?",
        "options": [
            "== performs type coercion before comparison, whereas === strictly checks both value and data type without coercion",
            "=== assigns variable values, while == checks inequality",
            "== is for numbers only, while === is for string characters",
            "There is no difference; they are interchangeable in modern ECMAScript"
        ],
        "answer": 0,
        "explanation": "Strict equality (===) prevents unexpected type coercion bugs by asserting that both operands have identical types and values."
    },
    {
        "id": "FS_B04",
        "domain": "full_stack",
        "type": "basic",
        "question": "In React, what is the primary purpose of the `useState` Hook?",
        "options": [
            "To declare and preserve state variables within functional components across renders, providing a state updater function",
            "To make direct asynchronous database connections",
            "To compile CSS preprocessors into plain CSS",
            "To restart the Node.js web server process"
        ],
        "answer": 0,
        "explanation": "useState allows React functional components to declare reactive state values that trigger re-rendering when updated."
    },
    {
        "id": "FS_B05",
        "domain": "full_stack",
        "type": "basic",
        "question": "Which HTTP response status code indicates that the server cannot locate the requested endpoint or resource?",
        "options": ["404 Not Found", "200 OK", "301 Moved Permanently", "500 Internal Server Error"],
        "answer": 0,
        "explanation": "HTTP status 404 communicates that the origin server did not find a current representation for the target URI."
    },
    {
        "id": "FS_B06",
        "domain": "full_stack",
        "type": "basic",
        "question": "In RESTful API design, which HTTP verb is standard for submitting data to create a new resource on the server?",
        "options": ["POST", "GET", "DELETE", "HEAD"],
        "answer": 0,
        "explanation": "POST is designed for transmitting entity payloads to the server, typically resulting in resource creation."
    },
    {
        "id": "FS_B07",
        "domain": "full_stack",
        "type": "basic",
        "question": "In CSS Flexbox layout, which property aligns items along the cross axis (perpendicular to the main flex direction)?",
        "options": ["align-items", "justify-content", "flex-direction", "flex-wrap"],
        "answer": 0,
        "explanation": "justify-content controls alignment along the main axis, whereas align-items aligns items along the cross axis."
    },
    {
        "id": "FS_B08",
        "domain": "full_stack",
        "type": "basic",
        "question": "What is the Document Object Model (DOM) in web browsers?",
        "options": [
            "An object-oriented tree representation of the structured HTML document that scripts can query and manipulate dynamically",
            "A relational database engine built inside Chrome",
            "A backend networking protocol for transferring binary files",
            "A stylesheet compiler used by CSS"
        ],
        "answer": 0,
        "explanation": "The DOM represents web pages in memory as a tree of nodes and objects, allowing JavaScript to dynamically alter structure and style."
    },
    {
        "id": "FS_B09",
        "domain": "full_stack",
        "type": "basic",
        "question": "In backend web architectures (such as Express or Flask hooks), what is the function of Middleware?",
        "options": [
            "Functions executed during request-response lifecycles to inspect, modify, authenticate, or log HTTP requests before terminal route handlers",
            "Physical network cables connecting routers to servers",
            "Desktop graphics drivers on client computers",
            "A database backup script"
        ],
        "answer": 0,
        "explanation": "Middleware intercepts incoming requests to execute cross-cutting concerns like authentication, CSRF checks, and security headers."
    },
    {
        "id": "FS_B10",
        "domain": "full_stack",
        "type": "basic",
        "question": "What does the browser security standard CORS (Cross-Origin Resource Sharing) enforce?",
        "options": [
            "It restricts client scripts running on one origin from making unauthorized API requests to a different origin without explicit server headers",
            "It prevents users from using multiple browser tabs",
            "It encrypts hard drives on client computers",
            "It forces web pages to use HTTPS protocols only"
        ],
        "answer": 0,
        "explanation": "CORS uses HTTP headers to tell browsers whether a web application running at one origin has permission to access resources from another origin."
    },
    {
        "id": "FS_B11",
        "domain": "full_stack",
        "type": "basic",
        "question": "In React, how do 'props' differ fundamentally from component 'state'?",
        "options": [
            "Props are immutable inputs passed down from parent to child, whereas state is mutable and managed internally by the component",
            "Props are stored on the database server, whereas state is stored in cookies",
            "Props can only hold strings, while state holds numbers",
            "There is no difference; props and state are identical"
        ],
        "answer": 0,
        "explanation": "Props are read-only configuration passed from parents, whereas state represents local, reactive component data."
    },
    {
        "id": "FS_B12",
        "domain": "full_stack",
        "type": "basic",
        "question": "Which SQL statement is executed to insert new records into an existing database table?",
        "options": ["INSERT INTO", "ADD ROW", "APPEND RECORD", "UPDATE SET"],
        "answer": 0,
        "explanation": "INSERT INTO table_name (columns) VALUES (values) is the standard SQL syntax for adding new records."
    },
    {
        "id": "FS_P01",
        "domain": "full_stack",
        "type": "practical",
        "question": "A developer submits login credentials via HTTP GET: `/login?email=user@test.com&password=secret`. Why is this a severe security vulnerability?",
        "options": [
            "GET query parameters are exposed in server access logs, browser history, proxy caches, and Referer headers in plaintext",
            "HTTP GET requests cannot send text strings over the internet",
            "GET queries are limited to 10 characters maximum",
            "GET requests cannot reach web server backends"
        ],
        "answer": 0,
        "explanation": "Sensitive credentials must be transmitted in the body of HTTP POST requests over HTTPS to prevent leakage into URLs and server logs."
    },
    {
        "id": "FS_P02",
        "domain": "full_stack",
        "type": "practical",
        "question": "How does a Cross-Site Request Forgery (CSRF) token protect an application against unauthorized state-changing actions?",
        "options": [
            "By embedding a secret, unpredictable, session-bound token in forms that a third-party site cannot read due to same-origin restrictions",
            "By disabling JavaScript execution across the entire web browser",
            "By encrypting the database hard drive with AES-256",
            "By blocking all user requests originating from mobile devices"
        ],
        "answer": 0,
        "explanation": "Browsers automatically send cookies with cross-site requests; a CSRF token ensures the request originated intentionally from the trusted site's form."
    },
    {
        "id": "FS_P03",
        "domain": "full_stack",
        "type": "practical",
        "question": "In modern JavaScript, what is the cleanest pattern for executing an asynchronous fetch request while gracefully catching network errors?",
        "options": [
            "Using async/await wrapped in a try...catch block to handle resolved data and catch rejections",
            "Using synchronous while-loops to pause browser execution until data arrives",
            "Using goto statements and recursive function timers",
            "Executing eval() on the URL string"
        ],
        "answer": 0,
        "explanation": "async/await with try...catch allows clean, readable asynchronous error handling without callback nesting."
    },
    {
        "id": "FS_P04",
        "domain": "full_stack",
        "type": "practical",
        "question": "In React, why is mutating state directly (e.g. `items.push(newItem)`) an anti-pattern that leads to UI bugs?",
        "options": [
            "React determines re-renders by shallow reference comparison; mutating in-place does not change array references, so the UI fails to update",
            "JavaScript throws a syntax error when mutating array contents",
            "Direct array mutation erases local storage data",
            "React only allows numbers to be stored in arrays"
        ],
        "answer": 0,
        "explanation": "React depends on immutability to detect state changes; using setter functions with new array references triggers appropriate re-renders."
    },
    {
        "id": "FS_P05",
        "domain": "full_stack",
        "type": "practical",
        "question": "You are crafting a responsive navigation bar that switches from an horizontal desktop row to a mobile drawer below 768px. Which CSS rule is essential?",
        "options": [
            "@media (max-width: 768px) { ... }",
            "@viewport (orientation: landscape) { ... }",
            "z-index: -9999",
            "position: fixed; display: none;"
        ],
        "answer": 0,
        "explanation": "CSS Media Queries apply distinct style rules based on device characteristics like viewport width."
    },
    {
        "id": "FS_P06",
        "domain": "full_stack",
        "type": "practical",
        "question": "A user enters `test' OR '1'='1` into a login form. How do backend developers systematically eliminate this SQL Injection vulnerability?",
        "options": [
            "Use parameterized SQL queries (prepared statements) so user inputs are treated strictly as literal data, never executable SQL code",
            "Strip out the letters 'O' and 'R' with string replace functions",
            "Encode all form inputs into Base64 before concatenation",
            "Store database tables as unindexed plain text files"
        ],
        "answer": 0,
        "explanation": "Parameterized queries decouple query logic from data inputs, ensuring user strings cannot alter the SQL syntax structure."
    },
    {
        "id": "FS_P07",
        "domain": "full_stack",
        "type": "practical",
        "question": "A student web app takes 7 seconds to load on mobile due to unoptimized multi-megabyte hero images. What is the most effective frontend optimization?",
        "options": [
            "Convert images to modern formats (WebP/AVIF), provide responsive srcset dimensions, and add `loading=\"lazy\"`",
            "Convert all images to uncompressed raw BMP format",
            "Remove all CSS styling sheets from the HTML header",
            "Increase backend server RAM without changing images"
        ],
        "answer": 0,
        "explanation": "Modern compressed image formats with responsive sizing and native lazy-loading dramatically reduce page payload and initial load times."
    },
    {
        "id": "FS_P08",
        "domain": "full_stack",
        "type": "practical",
        "question": "Why must crucial operations like authorization, password hashing, and test retake restrictions be validated on the backend server?",
        "options": [
            "Because frontend client code can be easily manipulated, inspected, or completely bypassed by users using developer tools or direct HTTP clients",
            "Because web browsers are computationally incapable of evaluating date comparisons",
            "Because backend servers are always faster than client mobile devices",
            "Because frontend JavaScript cannot make API requests"
        ],
        "answer": 0,
        "explanation": "Client-side validation is solely for user convenience; the backend is the authoritative security boundary that must strictly enforce rules."
    }
]


# ============================================================================
# ASSESSMENT SAMPLING & RECOMMENDATION EVALUATION UTILITIES
# ============================================================================

def generate_assessment_question_set(seed=None):
    """
    Selects exactly 25 questions:
    - Exactly 5 questions from each of the 5 domains
    - For each domain: exactly 3 basic and 2 practical questions
    - Total: 15 basic, 10 practical questions
    - Shuffles the final question set order
    """
    rng = random.Random(seed)
    selected = []

    for domain_key in CAREER_DOMAINS.keys():
        domain_questions = [q for q in QUESTIONS if q["domain"] == domain_key]
        basic_pool = [q for q in domain_questions if q["type"] == "basic"]
        practical_pool = [q for q in domain_questions if q["type"] == "practical"]

        # Ensure pools are sufficiently large
        if len(basic_pool) < 3 or len(practical_pool) < 2:
            raise ValueError(f"Insufficient questions for domain: {domain_key}")

        selected.extend(rng.sample(basic_pool, 3))
        selected.extend(rng.sample(practical_pool, 2))

    # Shuffle the final 25 questions so domains are interweaved
    rng.shuffle(selected)
    return selected


def calculate_level(percentage):
    """Interprets percentage scores into proficiency levels."""
    if percentage >= 70:
        return "Strong Foundation"
    elif percentage >= 40:
        return "Developing"
    else:
        return "Beginner"


def evaluate_assessment(submitted_answers, question_ids, user_profile=None):
    """
    Evaluates student responses against correct answers.
    submitted_answers: dict mapping question_id -> chosen option index (0..3)
    question_ids: list of question_id strings that were served
    user_profile: dict with keys: 'technical_skills', 'interests', 'preferred_career'
    
    Returns:
    {
        'domain_scores': {domain_key: {'score': s, 'total': 5, 'percentage': p, 'level': lvl}},
        'total_score': total_correct,
        'total_questions': len(question_ids),
        'overall_percentage': pct,
        'recommended_career': domain_key,
        'alternative_career': domain_key or None,
        'recommendation_explanation': text,
        'skill_gap': {
            'already_have': [...],
            'need_improvement': [...],
            'should_learn_next': [...]
        }
    }
    """
    # Build lookup for questions served
    served_map = {q["id"]: q for q in QUESTIONS if q["id"] in question_ids}

    domain_counts = {k: {"correct": 0, "total": 0, "unversed": 0} for k in CAREER_DOMAINS.keys()}
    total_correct = 0
    total_unversed = 0

    for qid in question_ids:
        q = served_map.get(qid)
        if not q:
            continue
        domain_key = q["domain"]
        domain_counts[domain_key]["total"] += 1
        
        user_choice = submitted_answers.get(qid)
        if user_choice == "unversed":
            domain_counts[domain_key]["unversed"] += 1
            total_unversed += 1
        elif user_choice is not None:
            try:
                user_choice_idx = int(user_choice)
                if user_choice_idx == q["answer"]:
                    domain_counts[domain_key]["correct"] += 1
                    total_correct += 1
            except (ValueError, TypeError):
                pass

    domain_scores = {}
    for dom_k, counts in domain_counts.items():
        total = counts["total"] or 5
        correct = counts["correct"]
        pct = round((correct / total) * 100, 1)
        domain_scores[dom_k] = {
            "title": CAREER_DOMAINS[dom_k]["title"],
            "score": correct,
            "total": total,
            "percentage": pct,
            "level": calculate_level(pct),
            "unversed": counts.get("unversed", 0)
        }

    total_questions = len(question_ids) or 25
    overall_percentage = round((total_correct / total_questions) * 100, 1)

    # Determine highest scoring domain(s)
    max_score = -1
    for dom_k, data in domain_scores.items():
        if data["score"] > max_score:
            max_score = data["score"]

    top_candidates = [k for k, v in domain_scores.items() if v["score"] == max_score]

    # Resolve tie-breaking if multiple top candidates exist
    user_skills = []
    user_interests = []
    preferred_career = None
    if user_profile:
        user_skills = user_profile.get("technical_skills", []) or []
        user_interests = user_profile.get("interests", []) or []
        preferred_career = user_profile.get("preferred_career")

    # Tie-break scoring
    def tie_break_score(dom_key):
        score = 0
        domain_meta = CAREER_DOMAINS[dom_key]
        # Check skill overlap
        for s in domain_meta["core_skills"]:
            if s in user_skills:
                score += 1
        # Check interest alignment
        for interest in user_interests:
            associated = INTEREST_TO_DOMAINS.get(interest, [])
            if dom_key in associated:
                score += 2
        # Explicit preferred career match
        if preferred_career == dom_key:
            score += 3
        return score

    sorted_candidates = sorted(top_candidates, key=lambda k: (tie_break_score(k), domain_scores[k]["score"]), reverse=True)
    recommended_career = sorted_candidates[0]
    
    # Identify alternative career
    alternative_career = None
    if len(sorted_candidates) > 1:
        alternative_career = sorted_candidates[1]
    else:
        # Pick the runner up from the remaining domains
        other_domains = [k for k in CAREER_DOMAINS.keys() if k != recommended_career]
        other_domains.sort(key=lambda k: domain_scores[k]["score"], reverse=True)
        if other_domains:
            alternative_career = other_domains[0]

    # Build human-readable explanation
    rec_title = CAREER_DOMAINS[recommended_career]["title"]
    rec_level = domain_scores[recommended_career]["level"]
    rec_score = domain_scores[recommended_career]["score"]
    
    explanation_parts = [
        f"Based on your assessment score of {rec_score}/5 ({domain_scores[recommended_career]['percentage']}%) "
        f"in the {rec_title} assessment, you demonstrated a '{rec_level}' foundation."
    ]
    if total_unversed > 0:
        explanation_parts.append(
            f"You selected 'Unversed' on {total_unversed} question{'s' if total_unversed > 1 else ''} for concepts you have not encountered yet; "
            f"no negative penalty was applied, and foundational prerequisites are prioritized in your roadmap."
        )
    if len(top_candidates) > 1:
        explanation_parts.append(
            f"You also scored equally well in other areas. We analyzed your stated technical skills and interests "
            f"to highlight {rec_title} as your highest-affinity starting point, while designating "
            f"{CAREER_DOMAINS[alternative_career]['title']} as your strong alternative career path."
        )
    else:
        explanation_parts.append(
            f"This domain represents your highest aptitude among the five evaluated fields. "
            f"Following the structured roadmap will systematically bridge remaining skill gaps."
        )
    explanation_text = " ".join(explanation_parts)

    # Compute Skill Gap for recommended career
    req_skills = CAREER_DOMAINS[recommended_career]["core_skills"]
    already_have = [s for s in req_skills if s in user_skills]
    
    # Skills you need to improve:
    # If student scored < 4 in this domain, or if they have listed the skill but domain score wasn't perfect
    if domain_scores[recommended_career]["score"] < 4:
        # Core skills that they already have or partially match need improvement
        need_improvement = [s for s in req_skills if s in already_have]
        should_learn_next = [s for s in req_skills if s not in already_have]
        if not need_improvement and req_skills:
            # If student has none of the skills, the first core skill is prioritized for improvement
            need_improvement = [req_skills[0]]
            should_learn_next = req_skills[1:]
    else:
        need_improvement = [s for s in req_skills if s not in already_have][:1]
        should_learn_next = [s for s in req_skills if s not in already_have and s not in need_improvement]

    return {
        "domain_scores": domain_scores,
        "total_score": total_correct,
        "total_questions": total_questions,
        "overall_percentage": overall_percentage,
        "recommended_career": recommended_career,
        "alternative_career": alternative_career,
        "recommendation_explanation": explanation_text,
        "skill_gap": {
            "already_have": already_have,
            "need_improvement": need_improvement,
            "should_learn_next": should_learn_next
        }
    }
