import pandas as pd
from metrics import linguistic, structural
from ast import literal_eval

if __name__ == '__main__':
    df = pd.read_csv('./results/conversations_heuristics1.csv', converters={"prompts": literal_eval,
                                                                 "answers": literal_eval,
                                                                 "prompts_codes": literal_eval,
                                                                 "prompts_errors": literal_eval,
                                                                 "answers_codes": literal_eval,
                                                                 "prompts_code_blocks": literal_eval})
    num_prim_quest_list = []
    num_prim_ks_ques_list = []
    num_acc_ans_list = []
    num_urls_list = []
    num_code_snippets_list = []
    mean_size_code_snippets_list = []
    num_api_calls_text_list = []
    num_api_calls_code_list = []
    code_descs_list = []
    se_words_list = []
    err_msgs_list = []
    distinct_words_list = []
    uniq_info_list = []
    misspelled_list = []
    incomplete_count_list = []
    complete_count_list = []
    total_text_speak_list = []
    ARI_list = []
    Coleman_Liau_list = []
    Flesch_reading_ease_list = []
    Flesch_Kincaid_grade_list = []
    Gunning_Fog_list = []
    Smog_list = []
    total_sent_list = []
    total_word_count_list = []
    for index, row in df.iterrows():
        num_prim_quest = 0
        num_prim_ks_ques = 0
        num_acc_ans = 0
        num_urls = 0
        num_code_snippets = 0
        mean_size_code_snippets = 0
        num_api_calls_text = 0
        num_api_calls_code = 0
        code_descs = 0
        se_words = 0
        err_msgs = 0
        distinct_words = 0
        uniq_info = 0
        misspelled = 0
        incomplete_count = 0
        complete_count = 0
        total_text_speak = 0
        ARI = 0
        Coleman_Liau = 0
        Flesch_reading_ease = 0
        Flesch_Kincaid_grade = 0
        Gunning_Fog = 0
        Smog = 0
        total_sent = 0
        total_word_count = 0

        # if row['ColumnID'] == 'prompts_fulltext_clean':
        full_clean_text = row['prompts_fulltext_clean']
        errors_list = row['prompts_errors']
        codes_list = row['prompts_codes']
        code_blocks_list = row['prompts_code_blocks']

        KnowledgeSeekingSharingClass = structural.KnowledgeSeekingSharing()
        ContextualClass = structural.Contextual()
        DiversityClass = linguistic.Diversity()
        ReadabilityClass = linguistic.Readability()
        VerbosityClass = linguistic.Verbosity()

        num_prim_quest, num_prim_ks_ques, num_acc_ans = (KnowledgeSeekingSharingClass.analyze(full_clean_text))
        (num_urls, num_code_snippets, mean_size_code_snippets, num_api_calls_code, num_api_calls_text, code_descs,
         se_words, err_msgs) = (ContextualClass.analyze(full_clean_text, errors_list, codes_list, code_blocks_list))
        distinct_words, uniq_info = DiversityClass.analyze(full_clean_text)
        (misspelled, incomplete_count, total_text_speak, ARI, Coleman_Liau,
         Flesch_reading_ease, Flesch_Kincaid_grade, Gunning_Fog, Smog) = ReadabilityClass.analyze(full_clean_text)
        total_sent, total_word_count = VerbosityClass.analyze(full_clean_text)

        num_prim_quest_list.append(num_prim_quest)
        num_prim_ks_ques_list.append(num_prim_ks_ques)
        num_acc_ans_list.append(num_acc_ans)
        num_urls_list.append(num_urls)
        num_code_snippets_list.append(num_code_snippets)
        mean_size_code_snippets_list.append(mean_size_code_snippets)
        num_api_calls_text_list.append(num_api_calls_text)
        num_api_calls_code_list.append(num_api_calls_code)
        code_descs_list.append(code_descs)
        se_words_list.append(se_words)
        err_msgs_list.append(err_msgs)
        distinct_words_list.append(distinct_words)
        uniq_info_list.append(uniq_info)
        misspelled_list.append(misspelled)
        incomplete_count_list.append(incomplete_count)
        complete_count_list.append(complete_count)
        total_text_speak_list.append(total_text_speak)
        ARI_list.append(ARI)
        Coleman_Liau_list.append(Coleman_Liau)
        Flesch_reading_ease_list.append(Flesch_reading_ease)
        Flesch_Kincaid_grade_list.append(Flesch_Kincaid_grade)
        Gunning_Fog_list.append(Gunning_Fog)
        Smog_list.append(Smog)
        total_sent_list.append(total_sent)
        total_word_count_list.append(total_word_count)

        # elif row['ColumnID'] == 'answers_fulltext_clean':
        # full_clean_text = row['answers_fulltext_clean']
        # errors_list = []
        # codes_list = row['answers_codes']
        # code_blocks_list = []
        #
        # KnowledgeSeekingSharingClass = structural.KnowledgeSeekingSharing()
        # ContextualClass = structural.Contextual()
        # DiversityClass = linguistic.Diversity()
        # ReadabilityClass = linguistic.Readability()
        # VerbosityClass = linguistic.Verbosity()
        #
        # num_prim_quest, num_prim_ks_ques, num_acc_ans = (KnowledgeSeekingSharingClass.analyze(full_clean_text))
        # (num_urls, num_code_snippets, mean_size_code_snippets, num_api_calls_code, num_api_calls_text, code_descs,
        #  se_words, err_msgs) = (ContextualClass.analyze(full_clean_text, errors_list, codes_list, code_blocks_list))
        # distinct_words, uniq_info = DiversityClass.analyze(full_clean_text)
        # (misspelled, incomplete_count, total_text_speak, ARI, Coleman_Liau,
        #  Flesch_reading_ease, Flesch_Kincaid_grade, Gunning_Fog, Smog) = ReadabilityClass.analyze(full_clean_text)
        # total_sent, total_word_count = VerbosityClass.analyze(full_clean_text)
        #
        #     # print(full_clean_text)
        # num_prim_quest_list.append(num_prim_quest)
        # num_prim_ks_ques_list.append(num_prim_ks_ques)
        # num_acc_ans_list.append(num_acc_ans)
        # num_urls_list.append(num_urls)
        # num_code_snippets_list.append(num_code_snippets)
        # mean_size_code_snippets_list.append(mean_size_code_snippets)
        # num_api_calls_text_list.append(num_api_calls_text)
        # num_api_calls_code_list.append(num_api_calls_code)
        # code_descs_list.append(code_descs)
        # se_words_list.append(se_words)
        # err_msgs_list.append(err_msgs)
        # distinct_words_list.append(distinct_words)
        # uniq_info_list.append(uniq_info)
        # misspelled_list.append(misspelled)
        # incomplete_count_list.append(incomplete_count)
        # complete_count_list.append(complete_count)
        # total_text_speak_list.append(total_text_speak)
        # ARI_list.append(ARI)
        # Coleman_Liau_list.append(Coleman_Liau)
        # Flesch_reading_ease_list.append(Flesch_reading_ease)
        # Flesch_Kincaid_grade_list.append(Flesch_Kincaid_grade)
        # Gunning_Fog_list.append(Gunning_Fog)
        # Smog_list.append(Smog)
        # total_sent_list.append(total_sent)
        # total_word_count_list.append(total_word_count)

    df['num_prim_quest'] = num_prim_quest_list
    df['num_prim_ks_ques'] = num_prim_ks_ques_list
    df['num_acc_ans'] = num_acc_ans_list
    df['num_urls'] = num_urls_list
    df['num_code_snippets'] = num_code_snippets_list
    df['mean_size_code_snippets'] = mean_size_code_snippets_list
    df['num_api_calls_text'] = num_api_calls_text_list
    df['num_api_calls_code'] = num_api_calls_code_list
    df['code_descs'] = code_descs_list
    df['se_words'] = se_words_list
    df['err_msgs'] = err_msgs_list
    df['distinct_words'] = distinct_words_list
    df['uniq_info'] = uniq_info_list
    df['misspelled'] = misspelled_list
    df['incomplete_count'] = incomplete_count_list
    df['complete_count'] = complete_count_list
    df['total_text_speak'] = total_text_speak_list
    df['ARI'] = ARI_list
    df['Coleman_Liau'] = Coleman_Liau_list
    df['Flesch_reading_ease'] = Flesch_reading_ease_list
    df['Flesch_Kincaid_grade'] = Flesch_Kincaid_grade_list
    df['Gunning_Fog'] = Gunning_Fog_list
    df['Smog'] = Smog_list
    df['total_sent'] = total_sent_list
    df['total_word_count'] = total_word_count_list

    df.to_csv('./results/conversations_heuristics.csv')
