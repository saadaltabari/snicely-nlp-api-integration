from googleapiclient import discovery


API_KEY = 'AIzaSyBi7L1viGhPzXoRH9sqfYZA1VsRAHRBS0U'

TOXICITY_THERESHOLD = 0.7

service = discovery.build(
    'commentanalyzer',
    'v1alpha1',
    developerKey=API_KEY,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False
)


def evaluate_text(text):
    request_body = {
        'comment': {
            'text': text
        },
        'requestedAttributes': {
            'TOXICITY': {
                'scoreThreshold': TOXICITY_THERESHOLD
            },
        },
        'spanAnnotations': True
    }

    response = service.comments().analyze(body=request_body).execute()
    toxic_text = []
    for highlighted_text in response.get('attributeScores', {}).get('TOXICITY', {}).get('spanScores', []):
        begin = highlighted_text['begin']
        end = highlighted_text['end']
        toxic_text.append({
            'text': text[begin:end],
            'begin': begin,
            'end': end
        })
    return toxic_text



if __name__ == '__main__':
    print("Try writing something..")
    text = input()
    result = evaluate_text(text)
    if not result:
        print("Way to go! you sure now how to communicate Snicely!")
    else:
        for highlighted_text in result:
            print(f'"{highlighted_text["text"]}" Oh oh! you are better than this.')
