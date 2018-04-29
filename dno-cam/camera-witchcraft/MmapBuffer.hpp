/*
 * MmapBuffer.hpp
 *
 *  Created on: 19 нояб. 2017 г.
 *      Author: snork
 */

#ifndef MMAPBUFFER_HPP_
#define MMAPBUFFER_HPP_

#include <linux/videodev2.h>

#include "../common/log.hpp"

namespace Cam
{

	class MmapBuffer: private Logable<MmapBuffer>
	{
	public:
		typedef decltype(v4l2_buffer().m.offset) offset_t;
		typedef decltype(v4l2_buffer().length) length_t;

		MmapBuffer();
		~MmapBuffer();

		MmapBuffer(const MmapBuffer & other) = delete;
		MmapBuffer & operator=(const MmapBuffer & other) = delete;

		MmapBuffer(MmapBuffer && other);
		MmapBuffer & operator=(MmapBuffer && other);

		void map(int fd, int index, offset_t offset, length_t len);
		void unmap();

		int index() const { return _index; }
		void * ptr() const { return _ptr; }
		length_t len() const { return _len; }

		friend void swap(MmapBuffer & left, MmapBuffer & right);

	private:
		void * _ptr = nullptr;
		length_t _len = 0;
		int _index = -1;
	};
}

#endif /* MMAPBUFFER_HPP_ */
