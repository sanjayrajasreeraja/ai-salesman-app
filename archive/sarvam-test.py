from sarvamai import SarvamAI

client = SarvamAI(
    api_subscription_key="sk_i1ktc73h_yN2h6WnULgJTi6wX4TvTh0DI",
)

response = client.speech_to_text.translate(
    file=open("/Users/amartyanambiar/Projects/AI Salesman/Recording (6).m4a", "rb"),
    model="saaras:v2.5"
)

print(response)
