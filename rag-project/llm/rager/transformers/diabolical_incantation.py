import hashlib

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def generate_document_id(doc):
    combined = f"{doc['course']}-{doc['question']}-{doc['text'][:10]}"
    hash_object = hashlib.md5(combined.encode())
    hash_hex = hash_object.hexdigest()
    document_id = hash_hex[:8]
    return document_id

@transformer
def transform(data, *args, **kwargs):
    print(f"Input data type: {type(data)}")
    print("Transformation input data:", data)
    
    documents = []

    if isinstance(data, list) and len(data) > 0:
        print("Input data is a non-empty list")
        for course_data in data:
            if isinstance(course_data, dict) and 'documents' in course_data:
                print("Processing course data:", course_data)
                course = course_data.get('course', 'unknown')
                for doc in course_data['documents']:
                    doc['course'] = course
                    doc['document_id'] = generate_document_id(doc)
                    documents.append(doc)
            else:
                print("Skipping invalid course data:", course_data)
    elif isinstance(data, dict) and 'documents' in data:
        print("Input data is a dictionary with 'documents' key")
        course = data.get('course', 'unknown')
        for doc in data['documents']:
            doc['course'] = course
            doc['document_id'] = generate_document_id(doc)
            documents.append(doc)
    else:
        print("Input data does not match the expected structure")

    print("Number of documents processed:", len(documents))

@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
    assert isinstance(output, list), 'The output should be a list'
    assert len(output) > 0, 'The output list should not be empty'
    for doc in output:
        assert 'document_id' in doc, 'Each document should have a document_id'
        assert 'course' in doc, 'Each document should have a course'
        assert 'question' in doc, 'Each document should have a question'
        assert 'text' in doc, 'Each document should have a text'
