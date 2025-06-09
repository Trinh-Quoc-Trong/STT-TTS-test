# -*- coding: utf-8 -*-
# <(6O9)>  
import os
from gtts import gTTS
from playsound import playsound  # Chuyển văn bản thành giọng nói  
import io             # Quản lý file trong bộ nhớ  
import threading      # Xử lý đa luồng để tăng tốc  

language_ = "vi"
text = (
r"""

Báo cáo chuyên sâu: Khơi dậy hứng thú và nhận diện dấu hiệu nghiện hành vi
I. Giới thiệu: Hành trình khám phá động lực và sự gắn kết

Hứng thú và ham muốn là những yếu tố then chốt định hình hành vi và trải nghiệm của con người, đóng vai trò là động lực cơ bản thúc đẩy sự học hỏi, phát triển và đạt được mục tiêu. Sự hiện diện của hứng thú và ham muốn lành mạnh không chỉ mang lại niềm vui, sự thỏa mãn mà còn là nguồn năng lượng tinh thần dồi dào, thúc đẩy sự sáng tạo và khả năng thích ứng với môi trường. Chúng là nền tảng cho một cuộc sống có ý nghĩa, giúp cá nhân vượt qua thử thách và kiến tạo giá trị cho bản thân và cộng đồng.

Tuy nhiên, ranh giới giữa một niềm đam mê lành mạnh và một hành vi nghiện ngập đôi khi rất tinh tế và dễ bị nhầm lẫn. Cả hai đều liên quan đến sự gắn kết sâu sắc với một hoạt động, nhưng chúng khác biệt cơ bản về bản chất và tác động lên cuộc sống cá nhân. Đam mê lành mạnh được định nghĩa là một sự lựa chọn tự nguyện, mang lại niềm vui, giá trị và sự thỏa mãn, đồng thời cho phép cá nhân có thể dừng lại hoặc điều chỉnh khi cần thiết. Ngược lại, nghiện ngập là một nhu cầu cưỡng bức, kiểm soát cá nhân, khiến họ khó lòng từ bỏ ngay cả khi nhận thức được những hậu quả tiêu cực.   

Sự khác biệt cốt lõi giữa đam mê và nghiện nằm ở khả năng kiểm soát của cá nhân đối với hành vi và tác động tổng thể của hành vi đó lên cuộc sống. Đam mê nâng cao giá trị cuộc sống và là một hành vi được lựa chọn, trong khi nghiện ngập phá vỡ các khía cạnh khác và mang tính cưỡng bức. Điều này cho thấy rằng ranh giới giữa hai khái niệm này không phải là nhị phân mà là một phổ liên tục, đòi hỏi sự tự nhận thức và đánh giá liên tục để phân biệt. Khi một hoạt động bắt đầu kiểm soát một người và lấy đi các lĩnh vực khác trong cuộc sống, đó là một dấu hiệu cho thấy nó đang chuyển từ đam mê sang nghiện.

II. Các yếu tố và phương pháp kích thích hứng thú, ham muốn

Để khơi dậy và duy trì hứng thú, ham muốn trong bất kỳ hoạt động nào, việc hiểu rõ nền tảng sinh học và tâm lý là vô cùng cần thiết.

2.1. Nền tảng sinh học của động lực: Vai trò của Dopamine và các Hormone

Dopamine là một chất dẫn truyền thần kinh và hormone hữu cơ quan trọng, được giải phóng chủ yếu bởi vùng dưới đồi tại não bộ. Khi nồng độ dopamine trong cơ thể tăng lên, nó mang lại cảm giác sảng khoái, thích thú, tràn đầy cảm hứng và động lực. Chất này đóng vai trò trung tâm trong nhiều chức năng quan trọng của cơ thể, bao gồm chuyển động, trí nhớ, và đặc biệt là hệ thống khen thưởng và động lực. Dopamine là một phần không thể thiếu trong hệ thống khen thưởng tự nhiên của cơ thể. Khi một người trải qua trạng thái hạnh phúc, đạt được mục tiêu hoặc nhận được phần thưởng, một lượng lớn dopamine sẽ được giải phóng vào não, tạo ra cảm giác hưng phấn và niềm vui. Chính cảm giác tích cực này thúc đẩy con người muốn lặp lại hành vi đó để tái tạo trải nghiệm tương tự.   

Dopamine hoạt động như một cơ chế củng cố thần kinh. Não bộ "học" cách liên kết các hoạt động nhất định với việc giải phóng dopamine, từ đó thúc đẩy mong muốn lặp lại chúng. Đây là cơ sở sinh học cho cả động lực lành mạnh và, khi bị rối loạn, là cơ chế hình thành nghiện. Cảm giác sảng khoái, thích thú, tràn đầy cảm hứng và động lực mà dopamine mang lại khiến cơ thể luôn muốn trải nghiệm cảm giác này nhiều hơn, tạo nên một vòng lặp học hỏi: hoạt động dẫn đến dopamine, dopamine dẫn đến khoái cảm, và khoái cảm dẫn đến mong muốn lặp lại hoạt động. Đây là cơ chế cốt lõi của sự củng cố hành vi.

Ham muốn và động lực không chỉ chịu ảnh hưởng của dopamine mà còn bởi sự cân bằng của các hormone khác và tình trạng sức khỏe thể chất tổng thể. Các hormone sinh dục như testosterone (ở cả nam và nữ) và estrogen (ở nữ) đóng vai trò quan trọng trong việc điều chỉnh ham muốn. Sự sụt giảm nồng độ các hormone này có thể dẫn đến giảm ham muốn đáng kể. Ngoài ra, sức khỏe tổng thể, bao gồm các trạng thái như mang thai, mãn kinh, các vấn đề về sức khỏe sinh sản (ví dụ: rối loạn cương dương), các bệnh lý toàn thân nghiêm trọng (như ung thư, bệnh thận), thiếu ngủ, căng thẳng kéo dài, trầm cảm, và tác dụng phụ của một số loại thuốc (điều trị tim mạch, huyết áp, trầm cảm) đều có thể làm suy giảm ham muốn và động lực. Việc lạm dụng rượu và các chất kích thích, mặc dù ban đầu có thể gây hưng phấn, nhưng về lâu dài sẽ làm suy yếu hệ thần kinh và gây tác dụng ngược, làm giảm ham muốn.   

Sự tương tác phức tạp giữa các yếu tố sinh học (hormone, sức khỏe thể chất) và tâm lý (căng thẳng, trầm cảm) là cực kỳ quan trọng đối với động lực. Điều này cho thấy một cách tiếp cận toàn diện đối với sức khỏe tổng thể là nền tảng để duy trì hứng thú và ham muốn bền vững. Ví dụ, khi cơ thể bị stress và căng thẳng kéo dài, một số hormone như cortisol và adrenaline được tiết ra, gây giảm ham muốn tình dục. Điều này minh họa mối liên hệ chặt chẽ giữa trạng thái tinh thần và cân bằng sinh lý. Việc giải quyết vấn đề động lực không chỉ là về khía cạnh tâm lý mà còn về việc duy trì một cơ thể khỏe mạnh và cân bằng nội tiết.   

Để tối ưu hóa mức dopamine một cách tự nhiên và bền vững, có nhiều phương pháp có thể áp dụng, liên quan trực tiếp đến các lựa chọn lối sống hàng ngày. Việc các lựa chọn lối sống lành mạnh, đơn giản có thể tác động trực tiếp đến nồng độ chất dẫn truyền thần kinh nhấn mạnh mối liên hệ sâu sắc giữa sức khỏe thể chất và động lực tinh thần. Điều này thay đổi nhận thức từ quan điểm cho rằng "động lực hoàn toàn là ý chí" sang nhận định rằng "động lực cũng là một trạng thái sinh hóa bị ảnh hưởng bởi thói quen hàng ngày."

Bảng 1: Các phương pháp tự nhiên để tối ưu hóa mức Dopamine

Phương pháp	Mô tả và Tác động	Nguồn tham khảo
Hoạt động thể chất	Tập thể dục, thiền, yoga, xoa bóp, đi dạo giúp tăng nồng độ dopamine, mang lại cảm giác vui vẻ và thư giãn.	
Thiết lập và đạt mục tiêu	Lập kế hoạch mục tiêu rõ ràng. Khi đạt được mục tiêu, cơ thể kích thích sản xuất thêm dopamine, củng cố động lực.	
Dinh dưỡng cân bằng	Bổ sung các vitamin và khoáng chất như sắt, niacin, folate, vitamin B6 hỗ trợ sản xuất dopamine.	
Tiếp xúc ánh nắng mặt trời	Giúp cơ thể hấp thụ đủ ánh sáng, kích thích sản xuất dopamine và cải thiện tâm trạng.	
Ngủ đủ giấc	Đảm bảo ngủ 7-9 giờ mỗi đêm giúp não hoạt động ổn định và duy trì mức dopamine cân bằng. Thiếu ngủ làm gián đoạn nhịp điệu tự nhiên này.	
Hoạt động thư giãn tâm trí	Thiền, vẽ tranh, âm nhạc, nhiếp ảnh, khiêu vũ giúp tăng mức dopamine và cải thiện tâm trạng.	
  
2.2. Động lực tâm lý nội tại: Thuyết Tự quyết (Self-Determination Theory)

Thuyết Tự quyết (Self-Determination Theory - SDT) là một mô hình tâm lý về động lực, tập trung vào ba nhu cầu tâm lý cốt lõi của con người: tự chủ (autonomy), năng lực (competence), và kết nối xã hội (relatedness). Khi những nhu cầu này được đáp ứng, cá nhân sẽ có động lực làm việc bền vững và hiệu suất cao hơn. SDT giúp các tổ chức hiểu cách tạo động lực nội tại bền vững cho nhân viên và xây dựng môi trường làm việc nơi nhân viên cảm thấy được trao quyền, có cơ hội phát triển và kết nối với đồng nghiệp.   

Quyền tự chủ (Autonomy): Cảm giác kiểm soát và lựa chọn hành vi.
Quyền tự chủ là nhu cầu cơ bản của con người muốn cảm thấy mình là người kiểm soát và có quyền lựa chọn trong các hành động và mục tiêu của chính mình, thay vì bị ép buộc hoặc kiểm soát từ bên ngoài. Khi một cá nhân cảm thấy có quyền tự chủ, họ sẽ cảm thấy công việc hoặc hoạt động đó là của mình, từ đó tăng cường sự chủ động, sáng tạo và trách nhiệm. Điều này trực tiếp dẫn đến việc tăng cường động lực nội tại. Trong thực tế, việc trao quyền ra quyết định, giảm kiểm soát vi mô, hoặc cho phép cá nhân tự chọn dự án hay lịch làm việc linh hoạt là những cách hiệu quả để tăng cường quyền tự chủ.   

Năng lực (Competence): Cảm giác thành thạo và khả năng phát triển kỹ năng.
Năng lực là nhu cầu cảm thấy mình có khả năng và hiệu quả trong việc thực hiện các nhiệm vụ, cũng như có cơ hội để học hỏi và phát triển các kỹ năng khác nhau. Khi cá nhân cảm thấy có năng lực, họ sẽ tự tin hơn vào khả năng của mình, dẫn đến sự hài lòng trong công việc và mong muốn tiếp tục học hỏi, cải thiện bản thân. Để thúc đẩy năng lực, cần cung cấp cơ hội phát triển kỹ năng, ví dụ như thiết lập các lộ trình phát triển nghề nghiệp phù hợp với sở thích và thế mạnh cá nhân. Việc học càng nhiều, càng sâu về một lĩnh vực yêu thích cũng sẽ giúp tăng cường cảm giác năng lực.   

Kết nối xã hội (Relatedness): Nhu cầu thuộc về và được hỗ trợ.
Kết nối xã hội là nhu cầu cảm thấy được kết nối, quan tâm và thuộc về một nhóm hoặc cộng đồng. Khi cá nhân cảm thấy có sự kết nối xã hội, họ sẽ cảm thấy được hỗ trợ, tin tưởng và có tinh thần đồng đội cao hơn, từ đó tăng cường sự gắn kết với tổ chức hoặc cộng đồng. Xây dựng một văn hóa làm việc cởi mở, hỗ trợ và tìm kiếm các mối quan hệ tích cực là những cách hiệu quả để đáp ứng nhu cầu này.   

Thuyết Tự quyết cung cấp một khuôn khổ mạnh mẽ để thiết kế các môi trường (làm việc, học tập, cuộc sống cá nhân) một cách tự nhiên thúc đẩy động lực nội tại. Nó chỉ ra rằng các phần thưởng bên ngoài (như tiền bạc) có thể làm suy yếu động lực nội tại nếu chúng làm giảm cảm giác tự chủ. Điều này ngụ ý rằng để duy trì sự gắn kết lâu dài, việc tập trung vào ba nhu cầu tâm lý này sẽ hiệu quả hơn là chỉ dựa vào các ưu đãi bên ngoài. Việc trao phần thưởng bên ngoài cho một hành vi có động cơ nội tại có thể làm suy yếu quyền tự chủ, một hiện tượng gọi là hiệu ứng quá mức. Khi hành vi ngày càng bị kiểm soát bởi phần thưởng bên ngoài, mọi người bắt đầu cảm thấy ít kiểm soát hành vi của mình hơn và động lực nội tại bị giảm đi. Điều này gợi ý một cách tiếp cận động lực tinh tế hơn, nơi các yếu tố thúc đẩy bên trong được ưu tiên để đảm bảo tính bền vững.   

2.3. Trạng thái dòng chảy (Flow State): Đỉnh cao của sự tập trung và hiệu suất

Trạng thái dòng chảy (Flow state) được định nghĩa là một trạng thái tâm trí mà trong đó cá nhân hoàn toàn tập trung duy nhất vào một hoạt động, quên mất cảm giác về không gian – thời gian và không còn nhận thức đến những xao nhãng bên ngoài. Nhà tâm lý học Mihaly Csikszentmihalyi, cha đẻ của khái niệm này, nhận định rằng trạng thái Flow giúp con người tăng trưởng và mãn nguyện khi họ sử dụng tối đa khả năng của mình trong một hoạt động.   

Các đặc điểm chính của Flow state bao gồm:

Tạo ra sự tập trung tuyệt đối: Toàn bộ sự chú ý và năng lượng đều được điều hướng vào một mục tiêu duy nhất của nhiệm vụ.   
Mục tiêu luôn hiện hữu và phản hồi tức thời: Tâm trí nhận diện chính xác mục đích của từng nhiệm vụ và sẵn sàng xử lý ngay lập tức.   
Cảm giác dễ dàng và không tốn sức: Các nhiệm vụ được xử lý nhanh chóng, ít nỗ lực hơn và đạt kết quả dễ dàng hơn.   
Nhận thức thời gian bị thay đổi: Thời gian có thể trôi nhanh hoặc chậm lại một cách bất thường mà không hề nhận thức được.   
Sự cân bằng giữa khả năng và độ khó của nhiệm vụ: Flow state chỉ xảy ra khi khả năng của một người tương ứng với độ khó của hoạt động đó. Nếu công việc quá dễ gây nhàm chán hoặc quá khó gây lo lắng, sự tập trung và hứng khởi sẽ không được duy trì.   
Tăng cảm giác mãn nguyện và hứng khởi: Cảm giác liên tục đạt được thành tựu và tiến bộ dẫn đến trạng thái hài lòng sâu sắc.   
Cảm giác kiểm soát hoàn toàn nhiệm vụ: Người tham gia cảm thấy kiểm soát cao nhất đối với nhiệm vụ, cho phép quá trình làm việc liên tục được định hình và điều chỉnh.   
Đạt được trạng thái Flow mang lại nhiều lợi ích đáng kể, đặc biệt trong công việc và học tập:

Nâng cao hiệu suất làm việc: Các nghiên cứu chỉ ra rằng Flow state giúp con người đạt hiệu suất làm việc cao hơn đáng kể so với thông thường (ví dụ: nghiên cứu của McKinsey cho thấy các CEO hàng đầu hiệu quả hơn tới 500% khi ở trạng thái Flow).   
Tăng trải nghiệm công việc: Mang lại những trải nghiệm tích cực và cảm giác thỏa mãn sâu sắc, khiến dòng chảy hứng thú và đam mê với công việc dâng trào.   
Cải thiện chất lượng công việc: Với sự tập trung cao độ và trải nghiệm tích cực, Flow state giúp cải thiện chất lượng đầu ra, kích thích sự sáng tạo và tận dụng tối đa kỹ năng cá nhân.   
Cải thiện sức khỏe tâm lý và tinh thần: Khi đạt Flow state, các khu vực não bộ liên quan đến ý thức và nhận thức môi trường "tắt đi," thay vào đó, các khu vực liên quan đến sự tập trung cao độ và tương tác tích cực trở nên mạnh mẽ. Các chất dẫn truyền thần kinh như norepinephrine, dopamine, serotonin, anandamide và endorphins được giải phóng, tạo cảm giác hưng phấn và mong muốn đắm chìm vào công việc hiện tại. Điều này giúp giảm xao nhãng bởi cảm xúc tiêu cực hay lo lắng.   
Trạng thái dòng chảy đại diện cho trạng thái gắn kết tối ưu nơi động lực nội tại được tối đa hóa. Sự cân bằng giữa thách thức và kỹ năng là một nguyên tắc thiết kế quan trọng cho các hoạt động nhằm duy trì sự gắn kết và ngăn ngừa sự nhàm chán (quá dễ) hoặc lo lắng (quá khó). Điều này cho thấy rằng việc điều chỉnh nhiệm vụ phù hợp với trình độ kỹ năng đang phát triển của một cá nhân là chìa khóa để nuôi dưỡng hứng thú lâu dài. Nếu một hoạt động quá dễ, nó sẽ gây nhàm chán; quá khó, nó sẽ gây thất vọng. Để giữ cho một người gắn kết và ở trạng thái "dòng chảy," hoạt động phải liên tục thích ứng với kỹ năng đang phát triển của họ, cung cấp đủ thách thức để thúc đẩy họ mà không làm họ quá tải. Đây là một trạng thái cân bằng động.

Đạt được trạng thái Flow không chỉ là một trải nghiệm thụ động mà là một quá trình chủ động rèn luyện. Các bước chi tiết để đạt được Flow State cho thấy nó đòi hỏi sự thiết kế môi trường có chủ đích, khả năng tự điều chỉnh và tự đánh giá liên tục. Điều này ngụ ý rằng các cá nhân có quyền tự chủ đáng kể trong việc nuôi dưỡng sự gắn kết sâu sắc của chính mình.

Bảng 2: Các yếu tố cần thiết và cách thực hành để đạt được Flow State

Yếu tố cần thiết	Cách thực hành để đạt được Flow State	Nguồn tham khảo
Sự cân bằng giữa thách thức và kỹ năng	Đánh giá kỹ năng hiện tại; điều chỉnh độ khó của nhiệm vụ (chia nhỏ hoặc nâng cao tiêu chuẩn); đảm bảo thách thức vừa đủ để kích thích nhưng không quá áp lực. Tránh ép bản thân làm việc vượt quá khả năng để không bị stress, và liên tục điều chỉnh theo tiến độ.	
Mục tiêu rõ ràng và phản hồi tức thời	Xác định mục tiêu cụ thể cho phiên làm việc (ví dụ: "Viết 1000 từ trong 2 giờ"); chia nhỏ mục tiêu lớn thành các phần rõ ràng; đặt thời hạn; thiết lập các điểm kiểm tra nhỏ để nhận phản hồi nhanh và liên tục về tiến độ. Tránh mục tiêu chung chung hoặc mơ hồ. Phản hồi nên rõ ràng, dễ hiểu và dễ áp dụng, tránh tự chỉ trích quá mức.	
Môi trường thuần khiết	Loại bỏ mọi xao nhãng (tắt điện thoại, thông báo mạng xã hội/email); tạo không gian làm việc thoải mái (yên tĩnh, đủ ánh sáng, nhiệt độ dễ chịu); chuẩn bị đầy đủ công cụ và sắp xếp bàn làm việc gọn gàng. Nếu không thể tránh tiếng ồn, sử dụng tai nghe chống ồn hoặc nhạc nền không lời.	
Tâm thế và sự chuẩn bị nội tại	Duy trì tâm trạng tích cực (không lo lắng hay căng thẳng); đảm bảo hoạt động xuất phát từ động lực nội tại (không phải áp lực bên ngoài); chọn thời điểm vàng khi năng lượng và sự tập trung ở đỉnh cao.	
Kỹ năng làm chủ bản thân	Rèn luyện khả năng kiểm soát suy nghĩ (hướng tâm trí vào một điểm); nhận biết khi nào đang vào Flow và khi nào mất đi nó; kiên nhẫn không ép buộc Flow; duy trì cảm giác kiểm soát và tự chủ. Tránh để áp lực từ người khác hoặc deadline làm mất kiểm soát.	
Áp dụng công nghệ và phần mềm quản lý công việc	Sử dụng các công cụ giúp tổ chức, theo dõi tiến độ và duy trì sự tập trung hiệu quả, giảm thiểu gián đoạn, tạo môi trường làm việc minh bạch và có kiểm soát.	
  
2.4. Các phương pháp thực tiễn để khơi dậy và duy trì hứng thú

Bên cạnh các cơ chế sinh học và tâm lý, việc áp dụng các phương pháp thực tiễn trong cuộc sống hàng ngày cũng đóng vai trò quan trọng trong việc khơi dậy và duy trì hứng thú. Các phương pháp này liên kết chặt chẽ với các nguyên tắc của Thuyết Tự quyết và điều kiện để đạt được Trạng thái dòng chảy.

Thiết lập mục tiêu rõ ràng, cụ thể và có ý nghĩa cá nhân.
Việc có mục tiêu rõ ràng, cụ thể và phù hợp với giá trị cá nhân là yếu tố then chốt để tạo động lực. Khi cá nhân biết chính xác mình đang hướng tới đâu, công việc sẽ trở nên có ý nghĩa và có hướng đi rõ ràng hơn, từ đó tạo động lực lớn để hành động. Ngược lại, việc đặt mục tiêu sai lầm, quá mơ hồ hoặc ôm đồm quá nhiều mục tiêu cùng lúc dễ dẫn đến cảm giác thất bại, chán nản và mất động lực cố gắng.   

Tạo môi trường thuận lợi và loại bỏ các yếu tố gây xao nhãng.
Môi trường xung quanh có ảnh hưởng lớn đến khả năng tập trung và hứng thú. Thiết kế một không gian học tập hoặc làm việc thoải mái, sáng tạo, đủ ánh sáng, gọn gàng và có tổ chức. Điều quan trọng là phải chủ động loại bỏ các yếu tố gây phiền nhiễu như điện thoại, thông báo mạng xã hội, email để đảm bảo sự tập trung tuyệt đối vào nhiệm vụ hiện tại.   

Áp dụng các phương pháp học tập/làm việc đa dạng và sáng tạo.
Sự đơn điệu dễ dẫn đến nhàm chán và mất hứng thú. Do đó, việc kết hợp các phương pháp đa dạng là cần thiết:

Trò chơi hóa (Gamification): Lồng ghép các trò chơi, mini-game vào quá trình học tập hoặc làm việc để làm cho chúng trở nên thú vị, thúc đẩy sự tham gia và phát triển kỹ năng.   
Kết hợp lý thuyết với thực tiễn: Áp dụng kiến thức vào các tình huống thực tế cuộc sống giúp cá nhân thấy được ý nghĩa và tính ứng dụng của những gì đang học/làm.   
Sử dụng hình ảnh, câu chuyện, bản đồ tư duy (Mindmap): Dẫn dắt nội dung thông qua các câu chuyện, hình ảnh minh họa hoặc sơ đồ tư duy giúp bài học trở nên mới lạ, hấp dẫn, dễ tiếp thu và ghi nhớ hơn.   
Tăng cường tương tác và làm việc nhóm: Tổ chức các hoạt động nhóm, thảo luận, thuyết trình, hoặc phân vai giúp học sinh/nhân viên tương tác lẫn nhau và với giáo viên/quản lý, rèn luyện kỹ năng giao tiếp và tư duy phản biện.   
Ghi nhận và tôn vinh những nỗ lực, thành tựu nhỏ.
Sự công nhận là một động lực mạnh mẽ. Khen ngợi và động viên kịp thời những nỗ lực, tiến bộ, dù là nhỏ nhất, giúp cá nhân cảm thấy được trân trọng, tự tin hơn và có thêm động lực để tiếp tục phấn đấu. Việc trưng bày các sản phẩm học tập hoặc thành quả công việc cũng tạo cảm giác hãnh diện và thúc đẩy sự cố gắng trong tương lai.   

Nuôi dưỡng sự tò mò, khám phá và chấp nhận thử thách phù hợp.
Sự tò mò là khởi nguồn của tri thức và hứng thú. Đặt những câu hỏi mở, khuyến khích cá nhân tự do đặt câu hỏi, tìm tòi và khám phá kiến thức mới. Đồng thời, công việc hoặc hoạt động cần có một chút thử thách để giữ được hứng thú và tránh sự nhàm chán. Mức độ thử thách phù hợp với năng lực sẽ thúc đẩy sự phát triển và duy trì sự gắn kết. Khuyến khích khám phá các chủ đề mà cá nhân thực sự say mê.   

Cá nhân hóa quá trình phát triển và học tập.
Mỗi cá nhân có sở thích, năng khiếu, điểm mạnh, điểm yếu khác nhau. Việc hiểu rõ những đặc điểm này  và điều chỉnh nội dung, phương pháp học tập/làm việc cho phù hợp sẽ giúp tăng cường hứng thú và hiệu quả. Khuyến khích cá nhân tự học, tự sắp xếp thời gian học tập và vui chơi, cũng như tham gia vào các hoạt động hỗ trợ gia đình để phát triển tính trách nhiệm và tự tin.   

Chăm sóc sức khỏe thể chất và tinh thần toàn diện.
Sức khỏe là nền tảng của mọi hoạt động. Đảm bảo ngủ đủ giấc (7-9 giờ mỗi đêm), ăn uống đúng cách, và tập thể dục nhẹ nhàng đều đặn để duy trì sức khỏe tốt, tinh thần tỉnh táo và có đủ năng lượng cho mọi hoạt động. Giảm căng thẳng và lo âu, tránh để tâm trí bị tiêu cực kéo dài, vì những yếu tố này có thể làm giảm đáng kể động lực.   

Các phương pháp thực tiễn này không phải là những lời khuyên riêng lẻ mà là các chiến lược liên kết với nhau, củng cố lẫn nhau để xây dựng động lực nội tại bền vững. Chúng thể hiện tầm quan trọng của quyền tự chủ, năng lực và kết nối xã hội từ Thuyết Tự quyết, cùng với các điều kiện để đạt được Trạng thái dòng chảy. Ví dụ, "cá nhân hóa quá trình học tập" liên quan đến quyền tự chủ; "ghi nhận thành tựu" liên quan đến năng lực; và "hoạt động nhóm" liên quan đến kết nối xã hội. "Tạo môi trường thuận lợi" và "chấp nhận thử thách phù hợp" là những điều kiện trực tiếp cho Trạng thái dòng chảy. Điều này cho thấy rằng lời khuyên thực tiễn không chỉ là những giai thoại mà còn dựa trên các lý thuyết tâm lý học đã được thiết lập, làm cho nó mạnh mẽ và hiệu quả hơn.

III. Nhận diện dấu hiệu trở nên nghiện một việc gì đó

Việc phân biệt giữa một niềm đam mê lành mạnh và một hành vi nghiện ngập là rất quan trọng để có thể can thiệp kịp thời và hiệu quả. Mặc dù cả hai đều liên quan đến sự gắn kết mạnh mẽ, nhưng có những dấu hiệu rõ ràng cho thấy một hành vi đã vượt quá ranh giới của sự lành mạnh.

3.1. Phân biệt rõ ràng giữa đam mê lành mạnh và nghiện ngập

Tiêu chí kiểm soát: Lựa chọn tự nguyện so với nhu cầu cưỡng bức.
Điểm khác biệt cơ bản nhất giữa đam mê và nghiện ngập nằm ở khả năng kiểm soát. Với đam mê, cá nhân cảm thấy đó là một sự lựa chọn tự nguyện, một hoạt động mang lại niềm vui và họ có thể dừng lại hoặc điều chỉnh khi cần thiết. Ngược lại, nghiện ngập được đặc trưng bởi cảm giác cưỡng bức, một nhu cầu mãnh liệt mà cá nhân khó có thể ngừng lại, ngay cả khi họ nhận thức được những hậu quả tiêu cực. Người nghiện thường mất khả năng kiểm soát hành vi, muốn dừng nhưng cơ thể và tâm trí không còn điều khiển được nữa.   

Tác động lên cuộc sống: Nâng cao giá trị so với gây gián đoạn và tổn hại.
Đam mê lành mạnh làm phong phú thêm cuộc sống, thêm giá trị và giúp cá nhân phát triển, cảm thấy viên mãn hơn. Ngược lại, khi một hoạt động trở thành nghiện, nó bắt đầu kiểm soát cá nhân, chiếm ưu tiên hơn các mối quan hệ quan trọng, công việc, học tập và thậm chí là sức khỏe. Nghiện ngập gây ra hàng loạt hậu quả tiêu cực nghiêm trọng về thể chất, tinh thần, xã hội, học tập và tài chính.   

Động lực cốt lõi: Niềm vui và sự phát triển so với trốn tránh và làm tê liệt cảm xúc.
Động lực thúc đẩy đam mê lành mạnh xuất phát từ niềm vui, sự hứng thú thực sự và mong muốn phát triển bản thân, khám phá những điều mới mẻ. Trong khi đó, hành vi nghiện ngập thường được sử dụng như một cơ chế đối phó để trốn tránh căng thẳng, nỗi buồn, sự lo âu, cảm giác trống rỗng, hoặc các vấn đề khó khăn trong cuộc sống. Hoạt động nghiện trở thành một cách để làm tê liệt hoặc tạm thời thoát ly khỏi những cảm xúc tiêu cực.   

Sự chuyển dịch quan trọng từ đam mê sang nghiện liên quan đến sự mất đi quyền tự chủ và tác động tiêu cực đến các chức năng tổng thể của cuộc sống. Vấn đề không chỉ nằm ở cường độ gắn kết, mà là lý do tại sao một người tham gia và những hy sinh nào được thực hiện. Điều này gợi ý rằng việc tự phản tư về động cơ và hậu quả là tối quan trọng để phát hiện sớm. Nếu một hoạt động, dù ban đầu có thú vị đến đâu, bắt đầu đóng vai trò là cơ chế đối phó chính cho những cảm xúc tiêu cực hoặc dẫn đến việc bỏ bê các lĩnh vực khác trong cuộc sống, đó là một dấu hiệu mạnh mẽ của một sự chuyển dịch có vấn đề.

3.2. Các triệu chứng và tiêu chí chẩn đoán nghiện hành vi

Các chứng nghiện hành vi, mặc dù không liên quan đến chất kích thích, nhưng có nhiều điểm tương đồng về cơ chế sinh hóa và tâm lý với rối loạn sử dụng chất gây nghiện. Trên thực tế, DSM-5 (Cẩm nang Chẩn đoán và Thống kê Rối loạn Tâm thần, ấn bản lần thứ 5) đã phân loại Rối loạn cờ bạc vào nhóm "Rối loạn liên quan đến chất và các rối loạn gây nghiện". Sự tương đồng của các tiêu chí này giữa nghiện chất và nghiện hành vi cho thấy một con đường sinh học thần kinh và tâm lý chung cho chứng nghiện, bất kể đối tượng cụ thể của sự nghiện là gì. Điều này ngụ ý rằng các biện pháp can thiệp cho nghiện hành vi có thể rút ra những điểm tương đồng từ việc điều trị lạm dụng chất. Hệ thống khen thưởng của não bộ và chu kỳ thèm muốn, dung nạp, cai nghiện và mất kiểm soát là những yếu tố cơ bản của chứng nghiện, dù đó là một chất hóa học hay một hành vi.   

Các triệu chứng và tiêu chí chẩn đoán phổ biến của nghiện hành vi bao gồm:

Mất khả năng kiểm soát hành vi: Cá nhân không thể dừng lại hoặc cắt giảm việc thực hiện hành vi nhất định, bất chấp nhận thức về những hậu quả tiêu cực mà nó gây ra. Người nghiện thường cảm thấy muốn dừng nhưng cơ thể và tâm trí không còn điều khiển được nữa, khả năng ra quyết định bị suy giảm.   
Bận tâm, ám ảnh quá mức về hành vi: Có những suy nghĩ, ký ức và sự thèm muốn mãnh liệt, ám ảnh về cảm giác có được từ hành vi đó. Hoạt động này chiếm một lượng lớn thời gian trong ngày của cá nhân, đến mức ngăn cản họ thực hiện các công việc hoặc hoạt động khác cần thiết hoặc mong muốn.   
Hiện tượng dung nạp (Tolerance): Cá nhân cần tăng cường mức độ tham gia vào hành vi (ví dụ: tăng thời gian, tần suất, cường độ) để đạt được hiệu ứng mong muốn hoặc cảm giác "phê" như ban đầu.   
Hội chứng cai (Withdrawal): Khi ngừng hoặc giảm hành vi, cá nhân trải qua các triệu chứng khó chịu về thể chất hoặc tâm lý, như lo lắng, bồn chồn, cáu kỉnh, thay đổi tâm trạng, sự thèm ăn và giấc ngủ bị rối loạn.   
Sao nhãng các hoạt động, trách nhiệm quan trọng khác: Cá nhân mất hứng thú với những sở thích, thú vui từng yêu thích trước đây. Họ đặt hành vi nghiện lên trên các yếu tố quan trọng khác của cuộc sống, bao gồm gia đình, công việc, học tập, và các mối quan hệ xã hội.   
Tiếp tục hành vi bất chấp nhận thức về hậu quả tiêu cực: Đây là một dấu hiệu cảnh báo nghiêm trọng, khi cá nhân vẫn tiếp tục thực hiện hành vi mặc dù họ biết rõ nó đang gây ra các vấn đề nghiêm trọng về sức khỏe (thể chất và tâm lý), xã hội, tài chính, hoặc pháp lý.   
Hành vi nói dối hoặc che giấu về mức độ tham gia: Cá nhân có xu hướng nói dối hoặc che giấu với gia đình, bạn bè, đồng nghiệp, hoặc các chuyên gia về mức độ tham gia vào hành vi nghiện của mình.   
Sử dụng hành vi như một cơ chế đối phó: Hành vi nghiện được sử dụng như một cách để trốn tránh hoặc làm dịu các cảm xúc tiêu cực như căng thẳng, nỗi buồn, lo âu, hoặc cảm giác bất lực.   
Các tiêu chí của DSM-5, mặc dù chi tiết, nhưng nhấn mạnh sự suy giảm chức năng và mất kiểm soát là yếu tố trung tâm để chẩn đoán. Việc một số tiêu chí (như "bận tâm" hoặc "trốn tránh") ít có tính dự đoán hơn đối với Rối loạn chơi game Internet (IGD) trong một số nghiên cứu  cho thấy rằng hậu quả và khả năng không thể dừng lại là những chỉ số đáng tin cậy hơn của chứng nghiện lâm sàng so với việc chỉ đơn thuần tham gia hoặc đối phó cảm xúc. Điều này ngụ ý rằng việc tự đánh giá nên xem xét kỹ lưỡng tác động gây rối loạn đến cuộc sống. Việc chỉ đơn thuần rất quan tâm hoặc sử dụng một hoạt động để thư giãn không nhất thiết là nghiện. Nghiện được chỉ ra mạnh mẽ hơn khi hoạt động bắt đầu thay thế các sở thích khác trong cuộc sống và tiếp tục bất chấp những tác hại rõ ràng. Điều này chuyển trọng tâm từ cảm xúc bên trong sang các tác động có hại, có thể quan sát được trong cuộc sống.   

Bảng 3: Các tiêu chí chẩn đoán phổ biến cho nghiện hành vi theo DSM-5

Rối loạn	Tiêu chí chẩn đoán theo DSM-5 (cần đạt số lượng nhất định trong 12 tháng)	Nguồn tham khảo
Rối loạn cờ bạc (Gambling Disorder) (Cần ít nhất 4/9 tiêu chí)	1. Cần đánh bạc với số tiền ngày càng tăng để đạt hưng phấn. <br> 2. Bồn chồn/cáu kỉnh khi cố gắng cắt giảm/ngừng đánh bạc. <br> 3. Nỗ lực không thành công để kiểm soát/cắt giảm/ngừng đánh bạc. <br> 4. Bận tâm quá mức với cờ bạc. <br> 5. Đánh bạc khi cảm thấy đau khổ. <br> 6. "Đuổi theo thua lỗ" (chasing losses). <br> 7. Nói dối để che giấu mức độ tham gia cờ bạc. <br> 8. Đánh bạc gây nguy hiểm hoặc mất các mối quan hệ/công việc/cơ hội. <br> 9. Dựa vào người khác để cung cấp tiền giải quyết tình hình tài chính do cờ bạc.	
Rối loạn chơi game Internet (Internet Gaming Disorder - IGD) (Cần ít nhất 5/9 tiêu chí)	1. Bận tâm quá mức với trò chơi Internet. <br> 2. Triệu chứng cai khi không được chơi game. <br> 3. Dung nạp: Cần tăng thời gian chơi game để đạt thỏa mãn. <br> 4. Mất kiểm soát: Nỗ lực không thành công để giảm/ngừng chơi game. <br> 5. Mất hứng thú với các hoạt động khác. <br> 6. Tiếp tục chơi game quá mức dù biết có vấn đề. <br> 7. Nói dối gia đình/bạn bè/chuyên gia về thời gian chơi game. <br> 8. Sử dụng game để trốn tránh/làm dịu cảm xúc tiêu cực. <br> 9. Gây nguy hiểm hoặc mất các mối quan hệ/công việc/cơ hội vì chơi game.	
  
3.3. Hậu quả tiêu cực của nghiện hành vi

Nghiện hành vi có thể gây ra những hậu quả nghiêm trọng và lan rộng, ảnh hưởng đến hầu hết các khía cạnh trong cuộc sống của một người. Hậu quả tiêu cực sâu rộng và đa diện trên các lĩnh vực thể chất, tinh thần, xã hội, học tập và tài chính nhấn mạnh rằng nghiện là một vấn đề mang tính hệ thống, không chỉ là một "thói quen xấu" cá nhân. Điều này ngụ ý rằng can thiệp hiệu quả đòi hỏi một cách tiếp cận toàn diện, đa lĩnh vực, giải quyết không chỉ hành vi nghiện mà còn cả những tác động lan tỏa của nó lên toàn bộ hệ thống cuộc sống của cá nhân.

Ảnh hưởng nghiêm trọng đến sức khỏe thể chất và tâm lý.

Thể chất: Nghiện có thể dẫn đến suy giảm sức khỏe thể chất nghiêm trọng, bao gồm sút cân nhanh chóng, thiếu ngủ kéo dài, mệt mỏi kiệt sức, suy yếu hệ thần kinh, tổn thương não bộ, và tăng nguy cơ tai nạn hoặc mắc các bệnh lý khác. Ví dụ điển hình là "miệng meth" (sâu răng, đen răng) ở người nghiện ma túy đá do vệ sinh kém và tác động của chất.   
Tâm lý: Các rối loạn tâm lý thường gặp bao gồm lo âu, trầm cảm, rối loạn giấc ngủ, hoang tưởng, rối loạn lưỡng cực. Cá nhân có thể mất kiểm soát cảm xúc, thể hiện hành vi bạo lực, tự hại bản thân, và có nguy cơ tự tử cao hơn. Sự cô lập xã hội cũng là một hệ quả tâm lý phổ biến.   
Sa sút hiệu suất trong học tập và công việc.
Nghiện hành vi làm giảm khả năng tập trung, ghi nhớ và xử lý thông tin, dẫn đến sa sút kết quả học tập và năng suất công việc. Thanh thiếu niên có nguy cơ bỏ học cao hơn và thường xuyên bị kỷ luật học đường. Người trưởng thành có thể gặp khó khăn trong việc duy trì vị trí công việc, thậm chí mất việc làm.   

Rạn nứt và cô lập trong các mối quan hệ xã hội và gia đình.
Hành vi nghiện ngập thường dẫn đến mâu thuẫn và rạn nứt trong gia đình, mất đi những người bạn tốt do ảnh hưởng tiêu cực đến hành vi và tính cách của người nghiện. Cá nhân có thể bị cô lập khỏi các hoạt động xã hội và cộng đồng, sống trong sự cô đơn và chán nản.   

Các vấn đề pháp lý và tài chính.
Khi tài nguyên tài chính cạn kiệt để duy trì hành vi nghiện, cá nhân có thể bị thúc đẩy thực hiện các hành vi phạm pháp như ăn cắp, lừa đảo, hoặc biển thủ. Họ cũng thường xuyên phải dựa vào người khác để cung cấp tiền giải quyết các tình huống tài chính tuyệt vọng do nghiện gây ra.   

3.4. Công cụ tự đánh giá và sàng lọc ban đầu

Việc nhận diện sớm các dấu hiệu nghiện là cực kỳ quan trọng để có thể can thiệp kịp thời và hiệu quả. Cá nhân có thể tự đánh giá hành vi của mình thông qua các câu hỏi tự vấn và các công cụ sàng lọc ban đầu. Sự sẵn có của các câu hỏi tự đánh giá và công cụ sàng lọc trao quyền cho các cá nhân chủ động theo dõi hành vi của họ. Điều này chuyển trách nhiệm từ việc chỉ chẩn đoán chuyên nghiệp sang sự cảnh giác cá nhân, thúc đẩy can thiệp sớm và tự quản lý. Việc nhấn mạnh vào "tại sao" một người tham gia (ví dụ: trốn tránh) là rất quan trọng để hiểu được sự dễ bị tổn thương tâm lý tiềm ẩn đối với chứng nghiện.

Các câu hỏi tự vấn quan trọng để nhận diện sớm nguy cơ.
Để tự kiểm tra xem một thói quen có đang chuyển thành nghiện hay không, một người có thể tự hỏi bản thân những câu hỏi sau:

Hành vi này đã trở thành cưỡng bức chưa? Có cảm thấy cần hoặc thèm muốn nó và mất khả năng dừng lại không?.   
Có bị bận tâm quá mức với hoạt động này, cả về mặt tinh thần hay thời gian nó chiếm dụng trong ngày, đến mức ngăn cản các công việc hoặc hoạt động khác cần thiết hoặc mong muốn không?.   
Có tiếp tục hành vi này mặc dù nó gây ra hậu quả tiêu cực về thể chất, tinh thần và/hoặc xã hội không?.   
Có những cảm xúc mạnh mẽ về hành vi này không? Nó có bắt nguồn từ cảm xúc và/hoặc dẫn đến cảm giác tội lỗi hay xấu hổ không? Có cảm thấy phòng thủ và chống đối khi xem xét hành vi của mình không?.   
Có hiện tượng dung nạp (cần tăng liều/cường độ để đạt hiệu ứng mong muốn) hoặc triệu chứng cai (khó chịu khi không thực hiện) không?.   
Có sử dụng hành vi này để trốn tránh các vấn đề hoặc làm tê liệt cảm xúc tiêu cực không?.   
Có đang hy sinh các mối quan hệ quan trọng hoặc sự bình yên nội tâm vì hành vi này không?.   
Giới thiệu về các công cụ sàng lọc hành vi tổng quát.
Các chuyên gia sử dụng nhiều công cụ để sàng lọc xu hướng nghiện hành vi. Một số công cụ phổ biến có thể được điều chỉnh để tự đánh giá hoặc sàng lọc ban đầu:

Behavior Risk Assessment Screen (BRAS): Công cụ này đánh giá xu hướng nghiện trên bảy lĩnh vực khác nhau: sử dụng chất (nicotine, rượu, ma túy, caffeine), thái độ ăn uống, tập thể dục, giấc ngủ, hành vi tình dục, cờ bạc và hành vi rủi ro (ví dụ: lái xe liều lĩnh). BRAS cung cấp một điểm số tổng thể phản ánh chức năng tâm lý, xã hội và nghề nghiệp của cá nhân.   
CAGE Assessment Tool (được điều chỉnh): Ban đầu được thiết kế để sàng lọc lạm dụng rượu, CAGE có thể được điều chỉnh để sàng lọc các hành vi gây nghiện khác bằng cách thay thế cụm từ "uống rượu" bằng hành vi cụ thể đang được đánh giá. Các câu hỏi tập trung vào việc:   
Có cảm thấy cần phải Cắt giảm (Cut down) hành vi này không?
Có cảm thấy Annoyed (khó chịu) hoặc tức giận khi người khác chỉ trích hành vi của mình không?
Có bao giờ cảm thấy Guilty (tội lỗi) về hành vi này không?
Có cần thực hiện hành vi này ngay sau khi thức dậy như một cách để Eye-opener (tỉnh táo) không?. Nếu trả lời "có" cho hai hoặc nhiều câu hỏi, có thể cần xem xét sâu hơn về nguy cơ nghiện.   
Các câu hỏi tự vấn và công cụ sàng lọc này được thiết kế để tự phản tư, bao gồm các tiêu chí chẩn đoán cốt lõi dưới dạng thân thiện với người dùng. Chúng trao quyền cho cá nhân tự hỏi mình những câu hỏi khó về kiểm soát, hậu quả và động lực. Điều này rất quan trọng để phát hiện sớm, vì nghiện thường liên quan đến sự phủ nhận.   

IV. Kết luận và khuyến nghị

Báo cáo này đã đi sâu vào các yếu tố và phương pháp để kích thích hứng thú và ham muốn, đồng thời cung cấp các tiêu chí rõ ràng để nhận diện khi một hành vi trở thành nghiện ngập. Hứng thú và động lực được thúc đẩy bởi sự cân bằng sinh học (đặc biệt là dopamine và các hormone khác) và việc đáp ứng các nhu cầu tâm lý cốt lõi như quyền tự chủ, năng lực và kết nối xã hội. Trạng thái dòng chảy (Flow State) là một đỉnh cao của sự gắn kết, nơi hiệu suất và sự thỏa mãn được tối ưu hóa. Ngược lại, nghiện là một trạng thái mất kiểm soát, được đặc trưng bởi sự ám ảnh, hiện tượng dung nạp, hội chứng cai, sự sao nhãng trách nhiệm và việc tiếp tục hành vi bất chấp những hậu quả tiêu cực. Sự khác biệt then chốt giữa đam mê lành mạnh và nghiện ngập nằm ở khả năng kiểm soát, tác động lên cuộc sống và động lực cốt lõi.

Để duy trì một cuộc sống cân bằng với sự gắn kết lành mạnh và phòng tránh nguy cơ nghiện ngập, các khuyến nghị sau được đưa ra:

Thúc đẩy hứng thú lành mạnh:

Chủ động tạo môi trường và điều kiện thuận lợi: Thiết lập không gian làm việc/học tập tối ưu, loại bỏ các yếu tố gây xao nhãng để tối đa hóa sự tập trung.
Thiết lập mục tiêu rõ ràng và có ý nghĩa: Đảm bảo mục tiêu cá nhân phù hợp với giá trị và khả năng, đồng thời chia nhỏ chúng để dễ dàng đạt được và nhận phản hồi tích cực.
Áp dụng đa dạng phương pháp: Kết hợp trò chơi hóa, hình ảnh, câu chuyện, và làm việc nhóm để giữ cho hoạt động luôn mới mẻ và hấp dẫn.
Ghi nhận và tôn vinh nỗ lực: Khen ngợi và động viên kịp thời các thành tựu, dù nhỏ, để củng cố sự tự tin và động lực.
Nuôi dưỡng sự tò mò và chấp nhận thử thách: Luôn tìm kiếm kiến thức mới và đặt ra những thách thức phù hợp với năng lực để duy trì sự hứng thú.
Cá nhân hóa quá trình phát triển: Điều chỉnh phương pháp và nội dung phù hợp với sở thích và năng lực cá nhân để tối ưu hóa hiệu quả.
Chăm sóc sức khỏe toàn diện: Đảm bảo đủ giấc ngủ, dinh dưỡng và tập thể dục đều đặn để duy trì nền tảng sinh học và tinh thần vững chắc cho động lực.
Nhận diện và phòng tránh nghiện ngập:

Tự vấn và đánh giá liên tục: Thường xuyên đặt câu hỏi về khả năng kiểm soát hành vi, động lực thực sự đằng sau nó (niềm vui hay trốn tránh), và tác động của nó lên các khía cạnh khác của cuộc sống.
Chú ý các dấu hiệu cảnh báo: Cảnh giác với các triệu chứng như mất kiểm soát, ám ảnh, hiện tượng dung nạp, hội chứng cai, sao nhãng trách nhiệm và tiếp tục hành vi bất chấp hậu quả tiêu cực.
Tìm kiếm hỗ trợ chuyên nghiệp: Nếu nhận thấy các dấu hiệu nghiện ngập hoặc gặp khó khăn trong việc tự kiểm soát, hãy tìm kiếm sự giúp đỡ từ các chuyên gia tâm lý, bác sĩ hoặc các tổ chức hỗ trợ. Can thiệp sớm là chìa khóa để điều trị hiệu quả và giảm thiểu hậu quả tiêu cực.
Hiểu rõ cơ chế của hứng thú và động lực, cùng với các dấu hiệu cảnh báo của nghiện ngập, sẽ giúp mỗi cá nhân chủ động xây dựng một cuộc sống phong phú, có ý nghĩa và cân bằng.







"""
)

def text_to_audio_play(text, language=language_): 
    save_path = r"D:\code\phanMemDoc\doc_len_001.mp3"
    # Chuyển văn bản thành file mp3 trong bộ nhớ  
    tts = gTTS(text=text, lang=language, slow=False)  
    tts.save(save_path) # lưu file mp3

    os.startfile(save_path)





def text_to_speech(text, language=language_):  
    # Chạy xử lý trong một thread để chương trình không bị chặn  
    threading.Thread(target=text_to_audio_play, args=(text, language)).start()  
text_to_speech(text)  # Gọi hàm đọc văn bản

