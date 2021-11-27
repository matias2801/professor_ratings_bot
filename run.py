from bot.professor_bot import ProfessorBot

with ProfessorBot() as bot:
    bot.land_first_page()
    bot.close_pop_up()
    bot.select_school()
    bot.view_top_professors()
    bot.get_all_professor_info()
    bot.report_results()