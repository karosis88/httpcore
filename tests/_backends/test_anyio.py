import ssl

import pytest

import httpcore


@pytest.mark.anyio
async def test_connect_without_tls(httpbin):
    backend = httpcore.AnyIOBackend()
    stream = await backend.connect_tcp(httpbin.host, httpbin.port)
    await stream.aclose()


@pytest.mark.anyio
async def test_write_without_tls(httpbin):
    backend = httpcore.AnyIOBackend()
    stream = await backend.connect_tcp(httpbin.host, httpbin.port)
    async with stream:
        http_request = [b"GET / HTTP/1.1\r\n", b"\r\n"]
        for chunk in http_request:
            await stream.write(chunk)


@pytest.mark.anyio
async def test_read_without_tls(httpbin):
    backend = httpcore.AnyIOBackend()
    stream = await backend.connect_tcp(httpbin.host, httpbin.port)
    http_request = [b"GET / HTTP/1.1\r\n", b"\r\n"]
    async with stream:
        for chunk in http_request:
            await stream.write(chunk)
        await stream.read(1024)


@pytest.mark.anyio
async def test_connect_with_tls(httpbin_secure):
    backend = httpcore.AnyIOBackend()
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    stream = await backend.connect_tcp(httpbin_secure.host, httpbin_secure.port)
    async with stream:
        tls_stream = await stream.start_tls(ssl_context=ssl_context)
        await tls_stream.aclose()


@pytest.mark.anyio
async def test_write_with_tls(httpbin_secure):
    backend = httpcore.AnyIOBackend()
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    stream = await backend.connect_tcp(httpbin_secure.host, httpbin_secure.port)
    async with stream:
        tls_stream = await stream.start_tls(ssl_context=ssl_context)
        async with tls_stream:
            http_request = [b"GET / HTTP/1.1\r\n", b"\r\n"]
            for chunk in http_request:
                await tls_stream.write(chunk)


@pytest.mark.anyio
async def test_read_with_tls(httpbin_secure):
    backend = httpcore.AnyIOBackend()
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    stream = await backend.connect_tcp(httpbin_secure.host, httpbin_secure.port)
    async with stream:
        tls_stream = await stream.start_tls(ssl_context=ssl_context)
        async with tls_stream:
            http_request = [b"GET / HTTP/1.1\r\n", b"\r\n"]
            for chunk in http_request:
                await tls_stream.write(chunk)
            await tls_stream.read(1024)
