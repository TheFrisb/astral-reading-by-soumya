up:
	sudo docker-compose up -d

down:
	sudo docker-compose down

clean-postgres:
	@echo "Stopping containers and removing the PostgreSQL volume..."
	-docker-compose down
	sudo docker volume rm astral-reading-by-soumya_astral-reading-by-soumya-postgres_data || echo "Volume already removed or does not exist."

clean:
	sudo docker stop $(sudo docker ps -aq)
	sudo docker rm $(sudo docker ps -aq)

build-serializers:
	cd ../frontend/lib && flutter pub run build_runner build --delete-conflicting-outputs



