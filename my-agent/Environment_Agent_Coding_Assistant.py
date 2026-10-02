from anthropic import Anthropic

client = Anthropic()


environment = client.beta.environments.create(
    name="quickstart-env",
    config={
        "type": "cloud",
        "networking": {"type": "limited", "allow_package_managers": True},
    },
)

print(f"Environment ID: {environment.id}")