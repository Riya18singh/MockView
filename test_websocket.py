import asyncio
import websockets
import json


async def test_interview():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgxMDEwMDk5LCJpYXQiOjE3Nzg0MTgwOTksImp0aSI6IjM4MzZlNWIzNDBmMTQ1ZDRiYTMyMjJmZDBjNDI5ZTU2IiwidXNlcl9pZCI6Mn0.h6qwF1eVMC6c2d_RUAGEAh2bZ8s-Mf5i5dh0Kjabc2U"
    session_id = "12"

    url = f"ws://127.0.0.1:8000/ws/interview/{session_id}/?token={token}"

    print("Connecting...")

    async with websockets.connect(url) as ws:
        print("Connected!")

        msg = await ws.recv()
        print(f"Server: {msg}")

        # Begin interview
        await ws.send(json.dumps({"type": "begin_interview"}))
        print("Sent: begin_interview")

        # Get typing indicator
        msg = await ws.recv()
        print(f"Server: {msg}")

        # Get first question
        msg = await ws.recv()
        print(f"\nFIRST QUESTION: {msg}\n")

        # Send answer 1
        await asyncio.sleep(1)
        await ws.send(json.dumps({
            "type": "send_answer",
            "message": "I would use Kadane's algorithm. Initialize max_sum and current_sum. Iterate through array, current_sum = max(arr[i], current_sum + arr[i]). Update max_sum if current_sum is greater. Time complexity O(n)."
        }))
        print("Sent: Answer 1")

        # Receive all responses
        while True:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=30)
                data = json.loads(msg)
                print(f"\n[{data['type']}]: {data.get('message', data)}")
            except asyncio.TimeoutError:
                print("Done!")
                break


asyncio.run(test_interview())