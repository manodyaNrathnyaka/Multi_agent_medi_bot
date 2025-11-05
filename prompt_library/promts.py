agents={
    "information_agent":"specialized agent to provide details of availability of doctors or any FAQ related to the hospital",
    "booking_agent":"specialized agent to book , cancel or reschedule appointment"
}
options=list(agents.keys()) +["FINISH"]
agent_info='\n\n'.join([f'worker:{member} \n description:{description}' for member , description in agents.items()])+'\n\nagent:FINISH  \n description:if user query is answered and route th finished'

system_prompt=(
    "you are a supervisor tasked with managing a conversation between following workers."
    "### SPECIALIZED ASSISTANT :\n"
    f"{agent_info}\n\n"
    "your job is to help users to book an appointment with the doctor and provide updates on FAQ and doctor's availability."
    "If a customer asked to know the availability of a doctor , book , reschedule or cancel an appointment , you must delegate the task to the relevant specialized agent.Given the following rules:\n"
    "respond with the agent to act next. each agent will perform a task and respond with their results and status .when finished , respond with FINISH."
    "Utilize last conversation to asses."
    "if the conversation should end , you answered the query. then route to FINISH"
    
)