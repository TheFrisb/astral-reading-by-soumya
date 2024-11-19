up:
	sudo docker-compose up -d

down:
	sudo docker-compose down

clean-postgres:
	sudo docker volume rm backend_produp-postgres_data

clean-redis:
	sudo docker volume rm backend_produp-redis_data

clean:
	sudo docker stop $(sudo docker ps -aq)
	sudo docker rm $(sudo docker ps -aq)

build-serializers:
	cd ../frontend/lib && flutter pub run build_runner build --delete-conflicting-outputs



