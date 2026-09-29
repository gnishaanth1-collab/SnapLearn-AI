# Snapdragon / Qualcomm AI Hub plan

Qualcomm AI Hub provides optimized/validated models and Workbench tooling for Qualcomm
devices. For Windows on Snapdragon, the recommended path is to target the exact HP
Snapdragon hardware and use a compatible ONNX/QNN or other supported runtime.

## Steps
1. Identify the exact HP model and Snapdragon X Plus/X Elite/X2 Elite chip.
2. Install ARM64 Python 3.11+ if using native Windows ARM.
3. Install Qualcomm AI Hub tooling:
   pip install qai-hub
4. Configure your token:
   qai-hub configure --api_token YOUR_TOKEN
5. Inspect devices:
   qai-hub list-devices
6. Choose a compatible text-generation model from AI Hub.
7. For a custom model, compile/profile it with AI Hub Workbench for the target device.
8. Prefer a precompiled QNN ONNX artifact when it is supported for your model and deployment.
9. Configure:
   set SNAPLEARN_ONNX_MODEL=C:\SnapLearn\models\optimized_model.onnx
10. Open Snapdragon / AI Hub inside SnapLearn and record actual providers and latency.

## Competition evidence
Use real measurements only:
- HP model and Snapdragon chip
- model name/version
- runtime and precision
- latency
- memory
- CPU/NPU execution
- offline test
- before/after optimization

Do not invent benchmark numbers.
