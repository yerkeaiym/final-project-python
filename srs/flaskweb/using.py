# # def find_news(coin_name):
# #     url = 'https://coinmarketcap.com/currencies/' + coin_name + '/news'
# #
# #     service = Service(ChromeDriverManager().install())
# #     driver = webdriver.Chrome(service=service)
# #     driver.get(url)
# #
# #     page = driver.page_source
# #     page_soup = BeautifulSoup(page, 'html.parser')
# #     news = page_soup.find("div", {"class": "wav26n-1", "class": "gWmJSZ"})
# #
# #
# #
# def summarization(text):
#     ARTICLE = ' '.join(text)
#     ARTICLE = ARTICLE.replace('.', '.<eos>')
#     ARTICLE = ARTICLE.replace('?', '?<eos>')
#     ARTICLE = ARTICLE.replace('!', '!<eos>')
#     max_chunk = 500
#     sentences = ARTICLE.split('<eos>')
#     current_chunk = 0
#     chunks = []
#     for sentence in sentences:
#         if len(chunks) == current_chunk + 1:
#             if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
#                 chunks[current_chunk].extend(sentence.split(' '))
#             else:
#                 current_chunk += 1
#                 chunks.append(sentence.split(' '))
#         else:
#             print(current_chunk)
#             chunks.append(sentence.split(' '))
#
#     for chunk_id in range(len(chunks)):
#         chunks[chunk_id] = ' '.join(chunks[chunk_id])
#
#     res = summarizer(chunks, max_length=130, min_length=10, do_sample=False)
#     summarized_text = ' '.join([summ['summary_text'] for summ in res])
#
#
