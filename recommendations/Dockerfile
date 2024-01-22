FROM public.ecr.aws/docker/library/python:slim

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY recommendations/ /service/recommendations/
WORKDIR /service/recommendations
RUN python -m pip install --no-cache-dir --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
--grpc_python_out=. ../protobufs/recommendations.proto

ENTRYPOINT [ "python", "recommendations.py" ]