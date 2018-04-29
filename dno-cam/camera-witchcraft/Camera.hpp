/*
 * Webcam.hpp
 *
 *  Created on: 19 нояб. 2017 г.
 *      Author: snork
 */

#ifndef CAMERA_HPP_
#define CAMERA_HPP_

#include <errno.h>
#include <sys/stat.h>

#include <cstring>
#include <array>
#include <thread>
#include <string>
#include <vector>

#include <boost/asio/io_service.hpp>
#include <boost/asio/strand.hpp>
#include <boost/asio/posix/stream_descriptor.hpp>

#include <boost/optional.hpp>
#include <boost/signals2.hpp>

#include "../common/log.hpp"
#include "MmapBuffer.hpp"

namespace Cam
{

	//! Класс для работы с камерой через драйвер v4l2
	/*! Класс использует многопоточность и boost asio для отслеживаний событий устройства
	    для корректной работы, программа должна быть собрана с макросом BOOST_ASIO_DISABLE_EPOLL
	*/
	class Camera: private Logable<Camera>
	{
	public:
		//! Абстрактный класс - кадр, полученный от камеры
		class Frame
		{
		public:
			virtual ~Frame() = default;
			//! Указатель на массив данных кадра
			virtual const void * data() = 0;
			//! Размер блока данных кадра
			virtual size_t dataSize() = 0;
			//! Формат пикселей кадра
			virtual const struct v4l2_pix_format & pixFmt() = 0;
		};

	public:
		//! Конструктор.
		/*! Иницилизирует и запускает io треды */
		Camera();

		/*! По удалению объекта останаливает все потоки */
		~Camera();

		//! Открывает устройство камеры (как правильно это /dev/video0
		/* проверяет его на поддержку необходимых для работы этого класса операций */
		void open(const std::string & path);
		//! Устанавливает формат принимаеого видео
		/*! Устобы узнать допустимые форматы, можно выполнить в консоли
		    v4l2-ctl --list-formats-ext
		    в параметре v4l2_fourcc ождается макрос и <linux/videodev2.h> вида (например) V4L2_PIX_FMT_YUYV */
		void set_fmt(uint32_t xres, uint32_t yres, uint32_t v4l2_fourcc);

		//! Начало съемки! Происходит аллокация буферов и начало получения кадров в указанном формате
		/*! Класс будет дергать сигнал onFrame по получению очередного кадра. Дальнейшая съемка не будет проводиться, пока
		    фукция - обработчик сигнала не завершит работу */
		void start(size_t framebuffer_queue_size = 4);

		//! Конец съемки
		void stop();

		//! Закрытие устройства и освобождение всех его ресурсов
		void close();

		//! Сигнал, который вызывается по получению сообщения от камермы
		boost::signals2::signal<void(std::shared_ptr<Frame>)> on_frame;

	private:
		typedef std::vector<std::shared_ptr<MmapBuffer>> BufferPool;

		void _init_ios();
		void _deinit_ios();
		void _init_buffers_ws(size_t buffers_count);
		void _reset_buffers_ws();
		void _enqueue_buffer_ws(const MmapBuffer & buffer, bool force = false);
		void _do_read_ws();

		boost::asio::io_service _io;
		std::array<std::thread, 1> _io_threads;
		boost::optional<boost::asio::io_service::work> _work;
		boost::asio::io_service::strand _strand;
		boost::asio::posix::stream_descriptor _fd;

		struct v4l2_format _fmt;
		bool _started = false;
		BufferPool _buffers_pool;
	};
}

#endif /* CAMERA_HPP_ */
