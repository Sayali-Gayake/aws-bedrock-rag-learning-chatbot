#1 Import json and boto3
import json
import boto3
#2 Create client connection to Bedrock Service - Boto3 API agentic_retrieve_stream https://docs.aws.amazon.com/boto3/latest/reference/services/bedrock-agent-runtime/client/agentic_retrieve_stream.html?utm_source=chatgpt.com
client = boto3.client('bedrock-agent-runtime')

def lambda_handler(event, context):
#3 Read and store question: {"prompt": "..."}
    query = event.get('prompt')
    print(query)

    #4 Query KB and receive streaming response
    response = client.agentic_retrieve_stream(
        agenticRetrieveConfiguration={
            "foundationModelConfiguration": {
                "bedrockFoundationModelConfiguration": {
                    "modelConfiguration": {"modelArn": f"MODEL_ARN"}
                },
                "type": "BEDROCK_FOUNDATION_MODEL",
            },
            "foundationModelType": "CUSTOM",
        },
        generateResponse=True,  # generate an answer, not just retrieve
        messages=[{"role": "user", "content": {"text": query}}],
        retrievers=[
            {"configuration": {"knowledgeBase": {"knowledgeBaseId": "KB_ID"}}}
        ],
    )    
    print(f"Raw data retrieved from KB: {response}")        

    #5 Get final result
    for chunk in response["stream"]:
        print(f"Answer is chunk: {chunk}")

        if "result" in chunk:

            result = chunk["result"]

            # Complete generated answer
            answer = result["generatedResponse"]["answer"]
            print(f"Answer is: {answer}")

            # Citations
            citations = result["generatedResponse"].get(
                "citations", []
            )
            print(f"Citations are: {citations}")
            
            # Retrieved sources
            results = result.get("results", [])
            print(f"Results are: {results}")

#6 Return response
    return {
        "statusCode": 200,

        "body": json.dumps({
            "answer": answer,
            "citations": citations,
            "results": results
        }, default=str)
    }






