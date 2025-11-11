import asyncio

class ValidatorNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.received_artifacts = []

    async def receive(self, artifact):
        print(f"[{self.node_id}] Received artifact: {artifact}")
        self.received_artifacts.append(artifact)

validator_mesh = []

def register_validator(node_id):
    node = ValidatorNode(node_id)
    validator_mesh.append(node)
    return node

async def propagate_artifact(artifact: str):
    tasks = [node.receive(artifact) for node in validator_mesh]
    await asyncio.gather(*tasks)
