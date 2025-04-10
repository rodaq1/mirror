import speechrecognition as spr
import aiSetup as s
import ssl 
import asyncio

async def main():
    print(ssl.OPENSSL_VERSION)
    await spr.listener()

if __name__ == "__main__":
    asyncio.run(main())
    






