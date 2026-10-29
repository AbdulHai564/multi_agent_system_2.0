test_cases = [
    {
        "input": "can you tell me what is inside the csv",
        "expected_agent": "analyst",
        "expected_facts": [
            "Describe the CSV's actual contents based on the data available.",
            "Do not claim to have inspected a CSV if its contents are unavailable.",
        ],
        "task_success_criteria": [
            "Summarize what the CSV contains.",
            "Mention relevant columns, rows, or patterns when the data is available.",
            "Ask the user to provide the CSV if it is unavailable.",
        ],
    },
    {
        "input": "can you tell me if apple stocks would go up in 2027 based on previous updates",
        "expected_agent": "financial",
        "expected_facts": [
            "Past stock performance does not establish what Apple's stock will do in 2027.",
            "Any forecast should be presented as uncertain, with relevant risks.",
        ],
        "task_success_criteria": [
            "Address the requested outlook for Apple stock.",
            "Explain uncertainty and relevant factors or risks.",
            "Avoid presenting a prediction as guaranteed.",
        ],
    },
    {
        "input": "do you think i should make my own llm",
        "expected_agent": "debate",
        "expected_facts": [
            "The decision depends on the user's goals, budget, expertise, and use case.",
            "Building a model and using an existing model or API have different costs and trade-offs.",
        ],
        "task_success_criteria": [
            "Discuss meaningful pros, cons, or trade-offs.",
            "Give a reasoned recommendation or explain what information is needed to make one.",
        ],
    },
    {
        "input": "can you tell me if my profit will go up according to the data i provided",
        "expected_agent": "analyst",
        "expected_facts": [
            "A forecast should be based on the provided data.",
            "A forecast is uncertain and should not be presented as guaranteed.",
            "Do not claim to have analyzed data that is unavailable.",
        ],
        "task_success_criteria": [
            "Use the provided data to assess profit trends if it is available.",
            "Explain the basis and limitations of any forecast.",
            "Ask for the data if it is unavailable.",
        ],
    },
    {
        "input": "do you think with 1 million dollars i should start a farm and do a poultry business",
        "expected_agent": "debate",
        "expected_facts": [
            "A recommendation depends on location, costs, experience, demand, and operating plans.",
            "The response should consider risks as well as potential benefits.",
        ],
        "task_success_criteria": [
            "Evaluate the poultry-farm idea rather than only discuss farming in general.",
            "Cover practical considerations, risks, or trade-offs.",
            "Avoid treating success or a specific return as guaranteed.",
        ],
    },
    {
        "input": "what do you think is the main reason my business is taking a hit",
        "expected_agent": "analyst",
        "expected_facts": [
            "A data-based cause should be supported by the business data.",
            "Do not state a specific cause as certain without supporting evidence.",
        ],
        "task_success_criteria": [
            "Identify likely causes using available business data.",
            "Explain the evidence behind the analysis.",
            "Ask for relevant data if it is unavailable.",
        ],
    },
    {
        "input": "is anthropic gonna be successful in their ipo and should i invest",
        "expected_agent": "financial",
        "expected_facts": [
            "An IPO's success and future investment returns are uncertain.",
            "The response should distinguish company prospects from whether an investment suits this user.",
        ],
        "task_success_criteria": [
            "Address both the IPO outlook and the investment question.",
            "Explain relevant risks and uncertainty.",
            "Avoid guaranteeing performance or giving a personalized conclusion without necessary context.",
        ],
    },
    {
        "input": "which company in ai should i invest in. who do you think will win",
        "expected_agent": "financial",
        "expected_facts": [
            "No company is certain to win the AI market.",
            "Investment comparisons should consider risks, valuation, and the user's goals and time horizon.",
        ],
        "task_success_criteria": [
            "Discuss how to compare AI companies as investments.",
            "Explain uncertainty and relevant risks.",
            "Avoid guaranteeing a winner or future return.",
        ],
    },
    {
        "input": "according to my data do you think i should start selling more goods",
        "expected_agent": "analyst",
        "expected_facts": [
            "The recommendation should be based on the user's business data.",
            "Relevant factors may include demand, inventory, margins, and sales trends.",
            "Do not claim to have analyzed data that is unavailable.",
        ],
        "task_success_criteria": [
            "Use available data to assess whether selling more goods is supported.",
            "Explain the evidence and important trade-offs.",
            "Ask for the data if it is unavailable.",
        ],
    },
    {
        "input": "should i start a dog farm in china",
        "expected_agent": "debate",
        "expected_facts": [
            "The response should clarify what the user means by a dog farm if that affects the recommendation.",
            "Any business assessment should consider local laws, animal welfare, demand, and feasibility.",
        ],
        "task_success_criteria": [
            "Address the proposed business idea.",
            "Discuss relevant feasibility, ethical, legal, or operational considerations.",
            "Ask for clarification if the meaning of dog farm is ambiguous.",
        ],
    },
    {
        "input": "you think starting an ai agency for international clients a good idea?",
        "expected_agent": "debate",
        "expected_facts": [
            "The viability depends on the agency's niche, expertise, customer demand, and ability to deliver.",
            "International clients can introduce sales, payment, legal, and time-zone considerations.",
        ],
        "task_success_criteria": [
            "Evaluate the AI agency idea with relevant pros and cons.",
            "Give practical factors or next steps to validate the idea.",
            "Avoid promising that the business will succeed.",
        ],
    },
]