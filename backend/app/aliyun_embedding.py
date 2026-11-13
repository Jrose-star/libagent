import os
from typing import List
from chromadb.api.types import EmbeddingFunction, Embeddings


class AliyunDashScopeEmbedding(EmbeddingFunction):
    """
    阿里云 DashScope (百炼) 文本嵌入模型包装类
    符合 ChromaDB 的接口规范
    """

    def __init__(self, model: str = "qwen3.7-text-embedding", dimensions: int = 512):
        """
        初始化阿里云嵌入模型
        :param model: 模型名称，默认 text-embedding-v3
        :param dimensions: 输出向量维度，默认 512 (BGE-small-zh-v1.5 也是 512 维，可以无缝替换)
        """
        # 确保你设置了环境变量 DASHSCOPE_API_KEY，否则无法调用
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "未找到环境变量 DASHSCOPE_API_KEY。"
                "请在运行项目前，在终端设置：set DASHSCOPE_API_KEY=sk-你的API密钥"
            )

        import dashscope

        dashscope.api_key = self.api_key

        self.model = model
        self.dimensions = dimensions

    def __call__(self, input: List[str]) -> Embeddings:

        # 核心方法：接收文本列表，返回对应的向量列表

        if not input:
            return []

        from dashscope import TextEmbedding

        # 1. 调用 API
        response = TextEmbedding.call(
            model=self.model,
            input=input,
            parameters={"text_type": "query", "dimensions": self.dimensions},
        )

        # 2. 检查 API 是否调用成功
        if response.status_code != 200:
            print(f"阿里云 API 调用失败: {response.code} - {response.message}")
            # 这里可以选择抛错，或者返回空列表让程序不崩溃
            raise Exception(f"API 调用失败: {response.message}")

        # 3. 安全地提取向量
        embeddings = []
        if response.output and response.output.get("embeddings"):
            for item in response.output.get("embeddings", []):
                embeddings.append(item["embedding"])

        return embeddings
