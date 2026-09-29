import os, time, platform
from pathlib import Path

def diagnostics():
    info = {
        "OS": platform.platform(),
        "Machine": platform.machine(),
        "Processor": platform.processor() or "Unknown",
        "Python": platform.python_version(),
        "Configured model": os.getenv("SNAPLEARN_ONNX_MODEL", "Not configured"),
    }
    try:
        import onnxruntime as ort
        providers = ort.get_available_providers()
        info["ONNX Runtime"] = ort.__version__
        info["Execution providers"] = ", ".join(providers)
        info["QNN available"] = "QNNExecutionProvider" in providers
    except Exception as e:
        info["ONNX Runtime"] = f"Unavailable: {e}"
    return info

def benchmark():
    model_path = os.getenv("SNAPLEARN_ONNX_MODEL")
    if not model_path or not Path(model_path).exists():
        return {"status": "No ONNX model configured. Set SNAPLEARN_ONNX_MODEL."}
    try:
        import onnxruntime as ort
        import numpy as np
        sess = ort.InferenceSession(model_path, providers=ort.get_available_providers())
        feed = {}
        for x in sess.get_inputs():
            shape = [d if isinstance(d, int) else 1 for d in x.shape]
            if x.type == "tensor(float)":
                feed[x.name] = np.zeros(shape, dtype=np.float32)
            elif x.type == "tensor(int64)":
                feed[x.name] = np.zeros(shape, dtype=np.int64)
            elif x.type == "tensor(int32)":
                feed[x.name] = np.zeros(shape, dtype=np.int32)
            else:
                return {"status": f"Unsupported input type: {x.type}"}
        t0 = time.perf_counter()
        sess.run(None, feed)
        return {"status": "OK", "latency_ms": round((time.perf_counter()-t0)*1000, 2),
                "providers": sess.get_providers(), "model": model_path}
    except Exception as e:
        return {"status": f"Benchmark failed: {e}"}
