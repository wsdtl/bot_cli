import asyncio
import websockets
import time
import json

task = set()


async def stress_test_single_message(client_id, timeout=20):
    """单个客户端测试：连接、发送一条消息、断开"""
    uri = f"ws://localhost:8000/ws/bot/{client_id}"

    try:
        start_time = time.time()
        async with websockets.connect(uri) as websocket:
            connection_time = time.time() - start_time

            sub = await asyncio.wait_for(websocket.recv(), timeout)
            # 发送一条消息
            message = {"type": "chat", "message": f"你好 {client_id}"}

            await websocket.send(json.dumps(message))

            # 可选：等待响应
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout)
                print({"status": "success", "connection_time": connection_time, "response": json.loads(response)})
                return {"status": "success", "connection_time": connection_time, "response": json.loads(response)}

            except asyncio.TimeoutError:
                print({"status": "success_no_response", "connection_time": connection_time})
                return {"status": "success_no_response", "connection_time": connection_time}

    except Exception as e:
        return {"status": "failed", "error": str(e)}


async def run_simple_stress_test(total_clients: int, batch_size: int):
    """运行简单的压力测试"""
    print(f"Starting stress test with {total_clients} clients...")
    start_time = time.time()

    results = {"success": 0, "failed": 0, "success_no_response": 0, "connection_times": []}

    # 分批执行
    for i in range(0, total_clients, batch_size):
        batch_start = i
        batch_end = min(i + batch_size, total_clients)

        print(f"Processing clients {batch_start} to {batch_end-1}")

        tasks = []
        for j in range(batch_start, batch_end):
            tasks.append(stress_test_single_message(f"client_{j}"))
            task.add(tasks[-1])

        batch_results = await asyncio.gather(*tasks)

        for result in batch_results:
            if result["status"] == "success":
                results["success"] += 1
                results["connection_times"].append(result["connection_time"])
            elif result["status"] == "success_no_response":
                results["success_no_response"] += 1
                results["connection_times"].append(result["connection_time"])
            else:
                results["failed"] += 1

        # 短暂休息
        if batch_end < total_clients:
            await asyncio.sleep(0.5)

    end_time = time.time()
    total_time = end_time - start_time
    # await asyncio.sleep(10)  # 确保所有连接关闭

    # 打印结果
    print(f"\n=== STRESS TEST RESULTS ===")
    print(f"Total clients: {total_clients}")
    print(f"Successful with response: {results['success']}")
    print(f"Successful without response: {results['success_no_response']}")
    print(f"Failed: {results['failed']}")
    print(f"Success rate: {(results['success'] + results['success_no_response']) / total_clients * 100:.2f}%")
    print(f"Total time: {total_time:.2f}s")
    print(f"Connections/sec: {total_clients / total_time:.2f}")

    if results["connection_times"]:
        avg_connection_time = sum(results["connection_times"]) / len(results["connection_times"])
        print(f"Average connection time: {avg_connection_time:.3f}s")


if __name__ == "__main__":

    total_clients = 2000
    batch_size = 1000

    asyncio.run(run_simple_stress_test(total_clients, batch_size))
