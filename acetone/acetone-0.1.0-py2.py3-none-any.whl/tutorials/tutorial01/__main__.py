# This one imports the acetone container for this app called 'dependencies'.
from tutorials.tutorial01.dependencies import dependencies
# A dummy type
from tutorials.tutorial01.data_sender import DataSender
from tutorials.tutorial01.stdout_data_sender import StdoutDataSender
from tutorials.tutorial01.worker import Worker


def main():
    # Register an instance to be used by all, who use Dependency(DataSender).
    # Strings can be used instead of types, but not interchangeably.
    dependencies.register_instance(DataSender, StdoutDataSender())

    # This worker depends on DataSender.
    worker = Worker()
    worker.do_the_job()

if __name__ == '__main__':
    main()
