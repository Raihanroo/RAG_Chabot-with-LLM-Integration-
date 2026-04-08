"""
Simple test script for RAG Chatbot API
Run the API server first: python api.py
Then run this script: python test_api.py
"""

import requests
import time

BASE_URL = "http://localhost:8000"


def test_health_check():
    print("\n" + "="*50)
    print("TEST 1: Health Check")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def test_list_documents():
    print("\n" + "="*50)
    print("TEST 2: List Documents")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/documents")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Message: {data['message']}")
    print(f"Documents: {data['details']['documents']}")
    return response.status_code == 200


def test_ingest():
    print("\n" + "="*50)
    print("TEST 3: Ingest Documents")
    print("="*50)
    
    response = requests.post(f"{BASE_URL}/ingest")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Status: {data['status']}")
        print(f"Message: {data['message']}")
        print(f"Details: {data['details']}")
        return True
    else:
        print(f"Error: {response.json()}")
        return False


def test_ask_question(question):
    print("\n" + "="*50)
    print(f"TEST 4: Ask Question")
    print("="*50)
    print(f"Question: {question}")
    
    data = {
        "question": question,
        "session_id": "test_session"
    }
    
    response = requests.post(f"{BASE_URL}/ask", json=data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nAnswer: {result['answer']}")
        print(f"\nSources ({len(result['sources'])}):")
        for src in result['sources']:
            print(f"  - {src['file']}")
        return True
    else:
        print(f"Error: {response.json()}")
        return False


def test_upload_file(filepath):
    print("\n" + "="*50)
    print("TEST 5: Upload File")
    print("="*50)
    print(f"File: {filepath}")
    
    try:
        with open(filepath, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{BASE_URL}/upload", files=files)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.status_code == 200
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return False


def test_reset():
    print("\n" + "="*50)
    print("TEST 6: Reset Conversation")
    print("="*50)
    
    response = requests.delete(f"{BASE_URL}/reset")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def main():
    print("\n" + "="*60)
    print("  RAG CHATBOT API - TEST SUITE")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    print("Make sure the API server is running!")
    print("="*60)
    
    time.sleep(1)
    
    # Run tests
    results = []
    
    # Test 1: Health check
    results.append(("Health Check", test_health_check()))
    time.sleep(0.5)
    
    # Test 2: List documents
    results.append(("List Documents", test_list_documents()))
    time.sleep(0.5)
    
    # Test 3: Ingest (if documents exist)
    results.append(("Ingest Documents", test_ingest()))
    time.sleep(2)  # Wait for ingestion to complete
    
    # Test 4: Ask questions
    questions = [
        "When was Google founded?",
        "Tell me about Microsoft",
        "What is RAG?"
    ]
    
    for q in questions:
        results.append((f"Ask: {q[:30]}...", test_ask_question(q)))
        time.sleep(0.5)
    
    # Test 5: Reset
    results.append(("Reset Conversation", test_reset()))
    
    # Summary
    print("\n" + "="*60)
    print("  TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API server!")
        print("Make sure the API is running: python api.py")
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
