from langchain.prompts import PromptTemplate

mcq_prompt_template = PromptTemplate(
    template=(
        "Generate a UNIQUE {difficulty} multiple-choice question about {topic}.\n"
        "IMPORTANT: Create a diverse, specific question that covers different aspects of the topic.\n"
        "Ensure the question is distinct and not repetitive.\n\n"
        "Return ONLY a JSON object with these exact fields:\n"
        "- 'question': A clear, specific question that tests understanding\n"
        "- 'options': An array of exactly 4 plausible answers\n"
        "- 'correct_answer': One of the options that is the correct answer\n\n"
        "Example format:\n"
        '{{\n'
        '    "question": "What is the capital of France?",\n'
        '    "options": ["London", "Berlin", "Paris", "Madrid"],\n'
        '    "correct_answer": "Paris"\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["topic", "difficulty"]
)

mcq_prompt_with_context_template = PromptTemplate(
    template=(
        "Generate a UNIQUE {difficulty} multiple-choice question about {topic}.\n\n"
        "CRITICAL: Avoid generating questions similar to these already created:\n"
        "{previous_questions}\n\n"
        "Requirements:\n"
        "1. The question MUST cover a DIFFERENT aspect or concept\n"
        "2. DO NOT rephrase or slightly modify existing questions\n"
        "3. Focus on a distinct subtopic, feature, or use case\n"
        "4. Test different knowledge areas within the topic\n\n"
        "Return ONLY a JSON object with these exact fields:\n"
        "- 'question': A clear, specific question testing DIFFERENT knowledge\n"
        "- 'options': An array of exactly 4 plausible answers\n"
        "- 'correct_answer': One of the options that is the correct answer\n\n"
        "Example format:\n"
        '{{\n'
        '    "question": "What is the capital of France?",\n'
        '    "options": ["London", "Berlin", "Paris", "Madrid"],\n'
        '    "correct_answer": "Paris"\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["topic", "difficulty", "previous_questions"]
)

fill_blank_prompt_template = PromptTemplate(
    template=(
        "Generate a UNIQUE {difficulty} fill-in-the-blank question about {topic}.\n"
        "IMPORTANT: Create a diverse, specific question that covers different aspects of the topic.\n"
        "Ensure the question is distinct and not repetitive.\n\n"
        "Return ONLY a JSON object with these exact fields:\n"
        "- 'question': A sentence with '_____' marking where the blank should be\n"
        "- 'answer': The correct word or phrase that belongs in the blank\n\n"
        "Example format:\n"
        '{{\n'
        '    "question": "The capital of France is _____.",\n'
        '    "answer": "Paris"\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["topic", "difficulty"]
)

fill_blank_prompt_with_context_template = PromptTemplate(
    template=(
        "Generate a UNIQUE {difficulty} fill-in-the-blank question about {topic}.\n\n"
        "CRITICAL: Avoid generating questions similar to these already created:\n"
        "{previous_questions}\n\n"
        "Requirements:\n"
        "1. The question MUST cover a DIFFERENT aspect or concept\n"
        "2. DO NOT rephrase or slightly modify existing questions\n"
        "3. Focus on a distinct subtopic, feature, or use case\n"
        "4. Test different knowledge areas within the topic\n\n"
        "Return ONLY a JSON object with these exact fields:\n"
        "- 'question': A sentence with '_____' marking where the blank should be\n"
        "- 'answer': The correct word or phrase that belongs in the blank\n\n"
        "Example format:\n"
        '{{\n'
        '    "question": "The capital of France is _____.",\n'
        '    "answer": "Paris"\n'
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["topic", "difficulty", "previous_questions"]
)

tutor_system_prompt = (
    "You are an expert AI tutor with deep knowledge of programming, AI/ML frameworks, and technology. "
    "When asked about technical tools or frameworks, provide accurate, detailed comparisons. "
    "For questions about AI frameworks like CrewAI, LangGraph, LangChain, AutoGen, etc., explain their "
    "use cases, strengths, and differences clearly. "
    "If you genuinely don't know something, admit it honestly rather than guessing. "
    "Use clear examples and practical scenarios to illustrate concepts. "
    "Be encouraging and patient, adapting explanations to the student's level."
)