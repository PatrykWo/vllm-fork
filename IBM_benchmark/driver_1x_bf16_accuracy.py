import torch
import habana_frameworks.torch.core as htcore
 
import time
import random
import argparse
import contextlib
random.seed(42)
 
from vllm.entrypoints.llm import LLM
from vllm.sampling_params import SamplingParams
 
def get_prompt():
    assistant_adjectives = ['a helpful', 'a kind', 'an unhelpful', 'an uppercase-yelling', 'a mad', 'a wise']
    assistants = ['assistant', 'robot', 'nerd', 'simpleton', 'scientist', 'politician', 'troglodyte']
    subjects = ['the capital city of', 'the best thing about', 'the worst thing about', 'the most famous place in', 'the best national dish of', 'the government system of']
    countries = ['Aruba', 'Islamic Republic of Afghanistan', 'Republic of Angola', 'Anguilla', 'Åland Islands', 'Republic of Albania', 'Principality of Andorra', 'United Arab Emirates', 'Argentine Republic', 'Republic of Armenia', 'American Samoa', 'Antarctica', 'French Southern Territories', 'Antigua and Barbuda', 'Australia', 'Republic of Austria', 'Republic of Azerbaijan', 'Republic of Burundi', 'Kingdom of Belgium', 'Republic of Benin', 'Bonaire, Sint Eustatius and Saba', 'Burkina Faso', "People's Republic of Bangladesh", 'Republic of Bulgaria', 'Kingdom of Bahrain', 'Commonwealth of the Bahamas', 'Republic of Bosnia and Herzegovina', 'Saint Barthélemy', 'Republic of Belarus', 'Belize', 'Bermuda', 'Plurinational State of Bolivia', 'Federative Republic of Brazil', 'Barbados', 'Brunei Darussalam', 'Kingdom of Bhutan', 'Bouvet Island', 'Republic of Botswana', 'Central African Republic', 'Canada', 'Cocos (Keeling) Islands', 'Swiss Confederation', 'Republic of Chile', "People's Republic of China", "Republic of Côte d'Ivoire", 'Republic of Cameroon', 'Congo, The Democratic Republic of the', 'Republic of the Congo', 'Cook Islands', 'Republic of Colombia', 'Union of the Comoros', 'Republic of Cabo Verde', 'Republic of Costa Rica', 'Republic of Cuba', 'Curaçao', 'Christmas Island', 'Cayman Islands', 'Republic of Cyprus', 'Czech Republic', 'Federal Republic of Germany', 'Republic of Djibouti', 'Commonwealth of Dominica', 'Kingdom of Denmark', 'Dominican Republic', "People's Democratic Republic of Algeria", 'Republic of Ecuador', 'Arab Republic of Egypt', 'the State of Eritrea', 'Western Sahara', 'Kingdom of Spain', 'Republic of Estonia', 'Federal Democratic Republic of Ethiopia', 'Republic of Finland', 'Republic of Fiji', 'Falkland Islands (Malvinas)', 'French Republic', 'Faroe Islands', 'Federated States of Micronesia', 'Gabonese Republic', 'United Kingdom of Great Britain and Northern Ireland', 'Georgia', 'Guernsey', 'Republic of Ghana', 'Gibraltar', 'Republic of Guinea', 'Guadeloupe', 'Republic of the Gambia', 'Republic of Guinea-Bissau', 'Republic of Equatorial Guinea', 'Hellenic Republic', 'Grenada', 'Greenland', 'Republic of Guatemala', 'French Guiana', 'Guam', 'Republic of Guyana', 'Hong Kong Special Administrative Region of China', 'Heard Island and McDonald Islands', 'Republic of Honduras', 'Republic of Croatia', 'Republic of Haiti', 'Hungary', 'Republic of Indonesia', 'Isle of Man', 'Republic of India', 'British Indian Ocean Territory', 'Ireland', 'Islamic Republic of Iran', 'Republic of Iraq', 'Republic of Iceland', 'State of Israel', 'Italian Republic', 'Jamaica', 'Jersey', 'Hashemite Kingdom of Jordan', 'Japan', 'Republic of Kazakhstan', 'Republic of Kenya', 'Kyrgyz Republic', 'Kingdom of Cambodia', 'Republic of Kiribati', 'Saint Kitts and Nevis', 'Korea, Republic of', 'State of Kuwait', "Lao People's Democratic Republic", 'Lebanese Republic', 'Republic of Liberia', 'Libya', 'Saint Lucia', 'Principality of Liechtenstein', 'Democratic Socialist Republic of Sri Lanka', 'Kingdom of Lesotho', 'Republic of Lithuania', 'Grand Duchy of Luxembourg', 'Republic of Latvia', 'Macao Special Administrative Region of China', 'Saint Martin (French part)', 'Kingdom of Morocco', 'Principality of Monaco', 'Republic of Moldova', 'Republic of Madagascar', 'Republic of Maldives', 'United Mexican States', 'Republic of the Marshall Islands', 'Republic of North Macedonia', 'Republic of Mali', 'Republic of Malta', 'Republic of Myanmar', 'Montenegro', 'Mongolia', 'Commonwealth of the Northern Mariana Islands', 'Republic of Mozambique', 'Islamic Republic of Mauritania', 'Montserrat', 'Martinique', 'Republic of Mauritius', 'Republic of Malawi', 'Malaysia', 'Mayotte', 'Republic of Namibia', 'New Caledonia', 'Republic of the Niger', 'Norfolk Island', 'Federal Republic of Nigeria', 'Republic of Nicaragua', 'Niue', 'Kingdom of the Netherlands', 'Kingdom of Norway', 'Federal Democratic Republic of Nepal', 'Republic of Nauru', 'New Zealand', 'Sultanate of Oman', 'Islamic Republic of Pakistan', 'Republic of Panama', 'Pitcairn', 'Republic of Peru', 'Republic of the Philippines', 'Republic of Palau', 'Independent State of Papua New Guinea', 'Republic of Poland', 'Puerto Rico', "Democratic People's Republic of Korea", 'Portuguese Republic', 'Republic of Paraguay', 'the State of Palestine', 'French Polynesia', 'State of Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwandese Republic', 'Kingdom of Saudi Arabia', 'Republic of the Sudan', 'Republic of Senegal', 'Republic of Singapore', 'South Georgia and the South Sandwich Islands', 'Saint Helena, Ascension and Tristan da Cunha', 'Svalbard and Jan Mayen', 'Solomon Islands', 'Republic of Sierra Leone', 'Republic of El Salvador', 'Republic of San Marino', 'Federal Republic of Somalia', 'Saint Pierre and Miquelon', 'Republic of Serbia', 'Republic of South Sudan', 'Democratic Republic of Sao Tome and Principe', 'Republic of Suriname', 'Slovak Republic', 'Republic of Slovenia', 'Kingdom of Sweden', 'Kingdom of Eswatini', 'Sint Maarten (Dutch part)', 'Republic of Seychelles', 'Syrian Arab Republic', 'Turks and Caicos Islands', 'Republic of Chad', 'Togolese Republic', 'Kingdom of Thailand', 'Republic of Tajikistan', 'Tokelau', 'Turkmenistan', 'Democratic Republic of Timor-Leste', 'Kingdom of Tonga', 'Republic of Trinidad and Tobago', 'Republic of Tunisia', 'Republic of Türkiye', 'Tuvalu', 'Taiwan, Province of China', 'United Republic of Tanzania', 'Republic of Uganda', 'Ukraine', 'United States Minor Outlying Islands', 'Eastern Republic of Uruguay', 'United States of America', 'Republic of Uzbekistan', 'Holy See (Vatican City State)', 'Saint Vincent and the Grenadines', 'Bolivarian Republic of Venezuela', 'British Virgin Islands', 'Virgin Islands of the United States', 'Socialist Republic of Viet Nam', 'Republic of Vanuatu', 'Wallis and Futuna', 'Independent State of Samoa', 'Republic of Yemen', 'Republic of South Africa', 'Republic of Zambia', 'Republic of Zimbabwe']
    respond_with = ['two sentences', 'a short poem', 'a joke about it', 'a song', 'one word', 'an angry rant']
    return f"<s>[INST] <<SYS>You are {random.choice(assistant_adjectives)} {random.choice(assistants)}.<</SYS>>\n\What is {random.choice(subjects)} {random.choice(countries)}? Respond with {random.choice(respond_with)}. [/INST]\n"
 
def main():
    parser = argparse.ArgumentParser(
                    prog='vllm_offline_test',
                    description='Tests vLLM offline mode')
    parser.add_argument('-n', '--batch-size', type=int, default=4)
    parser.add_argument('-w', '--world-size', type=int, default=1)
    parser.add_argument('-m', '--model', type=str, default="mixtral-8x7b")
    parser.add_argument('-e', '--enforce-eager', action='store_true')
    parser.add_argument('-p', '--profiling', action='store_true')
    parser.add_argument('-g', '--gpu-mem-utilization', type=float, default=0.5)
    parser.add_argument('-b', '--block-size', type=int, default=128)
    parser.add_argument('-l', '--max-seq-len-to-capture', type=int, default=2048)
    parser.add_argument('--temperature', type=float, default=0.0)
    parser.add_argument('--max-tokens', type=int, default=2048)
     
     
    args = parser.parse_args()
 
    batch_size = args.batch_size
    world_size = args.world_size
    max_seq_len_to_capture = args.max_seq_len_to_capture
    temperature = args.temperature
    block_size = args.block_size
    enforce_eager = args.enforce_eager
    gpu_mem_utilization = args.gpu_mem_utilization
    profiling = args.profiling
    max_tokens = args.max_tokens
     
    model = ''
    if args.model == '7b':
        model = '/mnt/weka/data/pytorch/llama2/Llama-2-7b-chat-hf'
    elif args.model == '70b':
        model = '/mnt/weka/data/pytorch/llama2/Llama-2-70b-chat-hf'
    elif args.model == 'mixtral-8x7b':
        model = '/root/ckpt/models--mistralai--Mixtral-8x7B-Instruct-v0.1/snapshots/41bd4c9e7e4fb318ca40e721131d4933966c2cc1/'
    else:
        model = args.model
 
    prompts = [get_prompt() for _ in range(batch_size)]
 
    # Create a sampling params object.
    sampling_params = SamplingParams(max_tokens=max_tokens, temperature=temperature)
 
    # Create an LLM.
    llm = LLM(model=model, enforce_eager=enforce_eager, swap_space=0, dtype=torch.bfloat16, tensor_parallel_size=world_size, block_size=block_size, max_num_seqs=batch_size, gpu_memory_utilization=gpu_mem_utilization, max_seq_len_to_capture=max_seq_len_to_capture)
    # Generate texts from the prompts. The output is a list of RequestOutput objects
    # that contain the prompt, generated text, and other information.
    start = time.time()
    profile_ctx = contextlib.nullcontext()
    if profiling:
        profile_ctx = torch.profiler.profile(
            schedule=torch.profiler.schedule(wait=0, warmup=0, active=1, repeat=0),
            activities=[torch.profiler.ProfilerActivity.CPU, torch.profiler.ProfilerActivity.HPU],
            on_trace_ready=torch.profiler.tensorboard_trace_handler('vllm_logs', use_gzip=True), with_stack=True, with_modules=True, record_shapes=False, profile_memory=False)
    with profile_ctx as profiler: 
        outputs = llm.generate(prompts, sampling_params)
    end = time.time()
 
    # Print the outputs.
    #from vllm.transformers_utils.tokenizer import get_tokenizer
    #tokenizer = get_tokenizer(model)
    total_time = end - start
    num_tokens = 0
    for output in outputs:
        prompt = output.prompt
        tokens = output.outputs[0].token_ids
        #decoded = tokenizer.decode(tokens)
        generated_text = output.outputs[0].text
        num_tokens += len(tokens)
        print(f"Prompt:\n\t{prompt!r}\nGenerated text:\n\t{generated_text!r}\ngen_len: {len(tokens)}\n")
    print(f"Gen tput: {num_tokens/total_time:.3f} tokens/s; Total tokens: {num_tokens}; total time: {total_time:.3f} seconds")
    print("VLLM HPU TEST: PASS")
 
if __name__ == '__main__':
    main()
